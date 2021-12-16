# import pickle as pkl

# train = pkl.load(open('./test_cls/meta.pkl', 'rb'))
# print(train)

# data = pkl.load(open('./test_cls/processed_data.pkl', 'rb'))
# print(data)



import pandas as pd
from dlkit.utils.logger import setting_logger
setting_logger('process.log')
from dlkit.utils.parser import config_parser_register
import copy
import json
import hjson
from dlkit.data.processors import processor_config_register, processor_register

# train_data = json.load(open('./local_data/tasks_data/title/title_train.json', 'r'))
# valid_data = json.load(open('./local_data/tasks_data/title/title_valid.json', 'r'))
# test_data = json.load(open('./local_data/tasks_data/title/title_test.json', 'r'))


# NER benchmark data
# train_data = json.load(open('./local_data/tasks_data/ner_benchmark/train.json', 'r'))
# valid_data = json.load(open('./local_data/tasks_data/ner_benchmark/valid.json', 'r'))
# test_data = json.load(open('./local_data/tasks_data/ner_benchmark/test.json', 'r'))
train_data = json.load(open('./examples/sequence_labeling/conll2003/data/train.json', 'r'))
valid_data = json.load(open('./examples/sequence_labeling/conll2003/data/valid.json', 'r'))
test_data = json.load(open('./examples/sequence_labeling/conll2003/data/test.json', 'r'))
data = {"predict": test_data}
# data = {"test": test_data}

inp = {"data": data}
# config = config_parser_register.get("processor")(hjson.load(open("./examples/sequence_labeling/conll2003/norm_lstm_crf/prepro.hjson"),object_pairs_hook=dict)).parser_with_check()[0]
config = config_parser_register.get("processor")(hjson.load(open("./examples/sequence_labeling/conll2003/norm_char_lstm_crf/prepro.hjson"),object_pairs_hook=dict)).parser_with_check()[0]
config['data_dir'] = 'test_predict'
# config = config_parser_register.get("processor")(hjson.load(open("./examples/sequence_labeling/conll2003/norm_lstm_crf/pre_prepro.hjson"),object_pairs_hook=dict)).parser_with_check()[0]

# print(json.dumps(config, indent=4))
processor_register.get(config.get('_name'))(stage="predict", config=processor_config_register.get(config.get('_name'))(stage="train", config=config)).process(inp)