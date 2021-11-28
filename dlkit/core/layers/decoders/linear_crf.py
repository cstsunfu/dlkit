import torch
from typing import Dict, List, Set
from dlkit.core.base_module import BaseModule, BaseModuleConfig
from . import decoder_register, decoder_config_register
from dlkit.core.modules import module_config_register, module_register
import copy

@decoder_config_register("linear_crf")
class LinearCRFConfig(BaseModuleConfig):
    """docstring for LinearCRFConfig
    {
        module@linear: {
            _base: linear,
        },
        module@crf: {
            _base: crf,
        },
        config: {
            input_size: "*@*",
            output_size: "*@*",
            return_logits: "decoder_logits",
            reduction: "mean",
            output_map: {}, //provide_key: output_key
            input_map: {} // required_key: provide_key
        },
        _link:{
            config.input_size: [module@linear.config.input_size],
            config.output_size: [module@linear.config.output_size, module@crf.config.output_size],
            config.reduction: [module@crf.config.reduction],
        }
        _name: "linear_crf",
    }
    """
    def __init__(self, config: Dict):
        super(LinearCRFConfig, self).__init__(config)
        self.linear_config = config["module@linear"]
        self.crf_config = config["module@crf"]
        self.return_logits = config['config']['return_logits']


@decoder_register("linear_crf")
class LinearCRF(BaseModule):
    def __init__(self, config: LinearCRFConfig):
        super(LinearCRF, self).__init__()
        self._provide_keys = {'logits', "predict_seq_label"}
        self._required_keys = {'embedding', 'label_ids', 'attention_mask'}
        self._provided_keys = set()

        self.config = config
        self.linear = module_register.get('linear')(module_config_register.get('linear')(config.linear_config))
        self.crf = module_register.get('crf')(module_config_register.get('crf')(config.crf_config))

    def forward(self, inputs: Dict[str, torch.Tensor])->Dict[str, torch.Tensor]:
        """
        """
        return self.predict_step(inputs)

    def predict_step(self, inputs: Dict[str, torch.Tensor])->Dict[str, torch.Tensor]:
        """predict
        :inputs: Dict[str: torch.Tensor], one mini-batch inputs
        :returns: Dict[str: torch.Tensor], one mini-batch outputs
        """

        logits = self.linear(inputs[self.get_input_name('embedding')])
        if self.config.return_logits:
            inputs[self.config.return_logits] = logits
        inputs[self.get_output_name("predict_seq_label")] = self.crf(logits, inputs[self.get_input_name('attention_mask')])
        return inputs

    def training_step(self, inputs: Dict[str, torch.Tensor])->Dict[str, torch.Tensor]:
        """TODO: Docstring for training_step.
        :arg1: TODO
        :returns: TODO

        """
        logits = self.linear(inputs[self.get_input_name('embedding')])
        loss = self.crf.training_step(logits, inputs[self.get_input_name('label_ids')], inputs[self.get_input_name('attention_mask')])
        if self.config.return_logits:
            inputs[self.config.return_logits] = logits
        inputs[self.get_output_name('loss')] = loss
        return inputs

    def validation_step(self, inputs: Dict[str, torch.Tensor])->Dict[str, torch.Tensor]:
        """TODO: Docstring for training_step.

        :arg1: TODO
        :returns: TODO

        """
        logits = self.linear(inputs[self.get_input_name('embedding')])
        loss = self.crf.training_step(logits, inputs[self.get_input_name('label_ids')], inputs[self.get_input_name('attention_mask')])
        if self.config.return_logits:
            inputs[self.config.return_logits] = logits
        inputs[self.get_output_name('loss')] = loss
        inputs[self.get_output_name("predict_seq_label")] = self.crf(logits, inputs[self.get_input_name('attention_mask')])
        return inputs
