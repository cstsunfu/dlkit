from transformers.models.roberta.modeling_roberta import RobertaModel
from transformers.models.roberta.configuration_roberta import RobertaConfig
import json

import os
import torch.nn as nn
import torch
from torch.nn.utils.rnn import pack_padded_sequence, pad_packed_sequence
from typing import Dict
from . import module_register, module_config_register

@module_config_register("roberta")
class RobertaWrapConfig(object):
    """docstring for RobertaWrapConfig
    {
        config: {
            "pretrained_model_path": "*@*",
        },
        _name: "roberta",
    }
    """

    def __init__(self, config: Dict):
        super(RobertaWrapConfig, self).__init__()
        self.pretrained_model_path = config['config']['pretrained_model_path']
        if os.path.isdir(self.pretrained_model_path):
            if os.path.exists(os.path.join(self.pretrained_model_path, 'config.json')):
                self.roberta_config = RobertaConfig(**json.load(open(os.path.join(self.pretrained_model_path, 'config.json'), 'r')))
            else:
                raise PermissionError(f"config.json must in the dir {self.pretrained_model_path}")
        else:
            if os.path.isfile(self.pretrained_model_path):
                try:
                    self.reberta_config = RobertaConfig(**json.load(open(self.pretrained_model_path, 'r')))
                except:
                    raise PermissionError(f"You must provide the pretrained model dir or the config file path.")
        

@module_register("roberta")
class RobertaWrap(nn.Module):
    def __init__(self, config: RobertaWrapConfig):
        super(RobertaWrap, self).__init__()

        self.roberta = RobertaModel(config.roberta_config, add_pooling_layer=False)

    def from_pretrained(self, pretrained_model_path):
        """TODO: Docstring for init.
        :pretrained_model_path: TODO
        :returns: TODO
        """
        self.roberta = RobertaModel.from_pretrained(pretrained_model_path)

    def forward(self, inputs):
        """
        """
        # No padding necessary.
        outputs = self.roberta(
            input_ids = inputs.get("input_ids", None),
            attention_mask = inputs.get("attention_mask", None),
            token_type_ids = inputs.get("token_type_ids", None),
            position_ids = inputs.get("position_ids", None),
            head_mask = inputs.get("head_mask", None),
            inputs_embeds = inputs.get("inputs_embeds", None),
            encoder_hidden_states = inputs.get("encoder_hidden_states", None),
            encoder_attention_mask = inputs.get("encoder_attention_mask", None),
            past_key_values = inputs.get("past_key_values", None),
            use_cache = inputs.get("use_cache", None),
            output_attentions = True,
            output_hidden_states = True,
            return_dict = False
        )
        sequence_output, _, all_hidden_states, all_self_attentions = outputs[0], outputs[1], outputs[3], outputs[4]
        return sequence_output, all_hidden_states, all_self_attentions