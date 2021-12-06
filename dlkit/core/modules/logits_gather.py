import torch.nn as nn
import torch
from typing import Dict, List
from . import module_register, module_config_register

@module_config_register("logits_gather")
class LogitsGatherConfig(object):
    """docstring for LogitsGatherConfig
    {
        "config": {
            "gather_layer": {
                "0": {
                    "map": "3", // the 0th layer not do scale output to "gather_logits_3", "gather_logits_" is the output name prefix, the "3" is map name
                    "scale": {} //don't scale
                },
                "1": {
                    "map": "4",  // the 1th layer scale output dim from 1024 to 200 and the output named "gather_logits_3"
                    "scale": {"1024":"200"},
                }
            },
            "prefix": "gather_logits_",
        },
        _name: "logits_gather",
    }
    """
    def __init__(self, config: Dict):
        super(LogitsGatherConfig, self).__init__()
        config = config.get('config', {})
        self.gather_layer = config.get('gather_layer', {})
        self.prefix = config.get("prefix", "gather_logits_")
        

@module_register("logits_gather")
class LogitsGather(nn.Module):
    def __init__(self, config: LogitsGatherConfig):
        super(LogitsGather, self).__init__()
        gather_layer_num = len(config.gather_layer)
        self.layers_scale = nn.ModuleDict()
        self.layer_map = {}
        self.prefix = config.prefix
        for layer, layer_config in config.gather_layer.items():
            self.layer_map[str(layer)] = str(layer_config['map'])
            if layer_config.get("scale", {}):
                scale = layer_config['scale']
                assert len(scale) == 1
                for from_dim, to_dim in scale.items:
                    self.layers_scale[str(layer)] = nn.Linear(int(from_dim), int(to_dim))


    def forward(self, input: List[torch.Tensor])->Dict[str, torch.Tensor]:
        """
        """
        # assert isinstance(input, List) or isinstance(input, tuple), f"type: {type(input)}, len: {len(input)}"
        result = {}
        for layer, layer_suffix in self.layer_map.items():
            result[self.prefix+layer_suffix] = self.layers_scale[layer](input[int(layer)])

        return result