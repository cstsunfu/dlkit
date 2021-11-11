from dlkit.utils.vocab import Vocabulary
from dlkit.utils.config import Config, GetConfigByStageMixin
from typing import Dict, Callable, Set, List
from dlkit.subprocessors import subprocessor_register, subprocessor_config_register, ISubProcessor

@subprocessor_config_register('token2id')
class Token2IDConfig(Config, GetConfigByStageMixin):
    """docstring for Token2IDConfig
        {
            "_name": "token2id",
            "config": {
                "train":{ //train、predict、online stage config,  using '&' split all stages
                    "data_pair": {
                        "label": "label_id"
                    },
                    "data_set": {                   // for different stage, this processor will process different part of data
                        "train": ['train', 'dev'],
                        "predict": ['predict'],
                        "online": ['online']
                    },
                    "vocab": "label_vocab", // usually provided by the "token_gather" module
                }, //3
                "predict": "train",
                "online": "train",
            }
        }
    """

    def __init__(self, stage, config: Dict):

        self.config = self.get_config(stage, config)
        self.data_set = self.config.get('data_set', {}).get(stage, [])
        self.data_pair = self.config.pop('data_pair', {})
        if self.data_set and (not self.data_pair):
            raise ValueError("You must provide 'data_pair' for token2id.")
        self.vocab = self.config.get('vocab', "")
        if self.data_set and (not self.vocab):
            raise ValueError("You must provide 'vocab' for token2id.")


@subprocessor_register('token2id')
class Token2ID(ISubProcessor):
    """docstring for Token2ID
    """

    def __init__(self, stage: str, config: Token2IDConfig):
        super().__init__()
        self.stage = stage
        self.config = config
        self.data_set = config.data_set
        self.data_pair = config.data_pair

    def process(self, data: Dict)->Dict:
        if not self.data_set:
            return data

        self.vocab = data[self.config.vocab]
        for data_set_name in self.data_set:
            data_set = data['data'][data_set_name]
            for key, value in self.data_pair.items():
                data_set[value] = data_set[key].parallel_apply(self.vocab.get_index, axis=1)
        return data