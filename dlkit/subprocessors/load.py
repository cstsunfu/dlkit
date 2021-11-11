from dlkit.utils.config import Config, GetConfigByStageMixin
from typing import Dict, Callable, Set, List
from dlkit.subprocessors import subprocessor_register, subprocessor_config_register, ISubProcessor
import pickle as pkl
import os


@subprocessor_config_register('load')
class LoadConfig(Config, GetConfigByStageMixin):
    """
    Config eg.
    {
        "_name": "load",
        "config":{
            "base_dir": "."
            "predict":{
                "token_ids": "./token_ids.pkl",
                "embedding": "./embedding.pkl",
                "label_ids": "./label_ids.pkl",
            },
            "online": [
                "predict", //base predict
                {   // special config, update predict, is this case, the config is null, means use all config from "predict", when this is empty dict, you can only set the value to a str "predict", they will get the same result
                }
            ]
        }
    },
    """

    def __init__(self, stage, config):
        self.config = self.get_config(stage, config)
        self.base_dir:str = config.get("base_dir", ".")


@subprocessor_register('load')
class Load(ISubProcessor):
    """
    """

    def __init__(self, stage: str, config: LoadConfig):
        super().__init__()
        self.stage = stage
        self.config = config.config
        self.base_dir = config.base_dir

    def load(self, path):
        """TODO: Docstring for load.
        """
        return pkl.load(open(os.path.join(self.base_dir, path), 'rb'))

    def process(self, data: Dict)->Dict:
        for key, value in self.config.items():
            data[key] = self.load(value)
        return data