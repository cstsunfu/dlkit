from dlkit.utils.vocab import Vocabulary
from dlkit.utils.config import BaseConfig, ConfigTool
from typing import Dict, Callable, Set, List
from dlkit.data.subprocessors import subprocessor_register, subprocessor_config_register, ISubProcessor
from functools import partial
import pandas as pd
from dlkit.utils.logger import logger

logger = logger()

@subprocessor_config_register('txt_reg_prepro')
class TxtRegPreProConfig(BaseConfig):
    """docstring for TxtRegPreProConfig
        {
            "_name": "txt_reg_prepro",
            "config": {
                "train":{ 
                    "data_set": {                   // for different stage, this processor will process different part of data
                        "train": ['train', 'valid', 'test', 'predict'],
                        "predict": ['predict'],
                        "online": ['online']
                    },
                    "input_map": {   // without necessery don't change this
                        "sentence": "sentence", //for single
                        "sentence_a": "sentence_a",  // for pair
                        "sentence_b": "sentence_b",
                        "uuid": "uuid",
                        "value": "value",
                    },
                    "output_map": {   // without necessery don't change this
                        "sentence": "sentence", //for single
                        "sentence_a": "sentence_a", //for pair
                        "sentence_b": "sentence_b",
                        "uuid": "uuid",
                        "value": "value",
                    },
                    "data_type": "single", // single or pair
                },
                "predict": "train",
                "online": "train",
            }
        }
        NOTE: the txt_regformat input is
        {
            "uuid": '**-**-**-**'
            "sentence": "I have an apple",
            "value":  0.0
        }
    """
    def __init__(self, stage, config: Dict):

        super(TxtRegPreProConfig, self).__init__(config)
        self.config = ConfigTool.get_config_by_stage(stage, config)
        self.data_set = self.config.get('data_set', {}).get(stage, [])
        if not self.data_set:
            return
        self.output_map = self.config['output_map']
        self.input_map = self.config['input_map']
        self.data_type = self.config['data_type']
        self.post_check(self.config, used=[
            "data_set",
            "output_map",
        ])


@subprocessor_register('txt_reg_prepro')
class TxtRegPrePro(ISubProcessor):
    """docstring for TxtRegPrePro
    """

    def __init__(self, stage: str, config: TxtRegPreProConfig):
        super().__init__()
        self.stage = stage
        self.config = config
        self.data_set = config.data_set
        self.data_type = config.data_type
        assert self.data_type in {'single', 'pair'}
        if not self.data_set:
            logger.info(f"Skip 'txt_reg_prepro' at stage {self.stage}")
            return

    def process(self, data: Dict)->Dict:
        '''
            data: {
                "train": list of json format train data
            }
        '''

        if not self.data_set:
            return data

        for data_set_name in self.data_set:
            if data_set_name not in data['data']:
                logger.info(f'The {data_set_name} not in data. We will skip do txt_reg_prepro on it.')
                continue
            data_set = data['data'][data_set_name]

            uuids = []
            values = []
            # for pair
            sentences_a = []
            sentences_b = []
            # for single
            sentences = []

            for one_ins in data_set:
                try:
                    if self.data_type == 'pair':
                        sentences_a.append(one_ins[self.config.input_map['sentence_a']])
                        sentences_b.append(one_ins[self.config.input_map['sentence_b']])
                    else:
                        sentences.append(one_ins[self.config.input_map['sentence']])
                    uuids.append(one_ins[self.config.input_map['uuid']])
                    values.append(one_ins[self.config.input_map['value']])
                except:
                    raise PermissionError(f"You must provide the data as requests, we need 'sentence', 'uuid' and 'labels', or you can provide the input_map to map the origin data to this format")
            if self.data_type == 'pair':
                data_df = pd.DataFrame(data= {
                    self.config.output_map["sentence_a"]: sentences_a,
                    self.config.output_map["sentence_b"]: sentences_b,
                    self.config.output_map["uuid"]: uuids,
                    self.config.output_map["values"]: values,
                })
            else:
                data_df = pd.DataFrame(data= {
                    self.config.output_map["sentence"]: sentences,
                    self.config.output_map["uuid"]: uuids,
                    self.config.output_map["values"]: values,
                })
            data['data'][data_set_name] = data_df

        return data