AttributeError: The base config and update config is not match. base: 
    {'data_set': {'train': ['train', 'valid', 'test', 'predict'], 'predict': ['predict'], 'online': ['online']}, 'config_path': '*@*', 'truncation': None, 'normalizer': 'default', 'pre_tokenizer': 'default', 'post_processor': 'default', 'output_map': {'tokens': 'tokens', 'ids': 'input_ids', 'attention_mask': 'attention_mask', 'type_ids': 'type_ids', 'special_tokens_mask': 'special_tokens_mask', 'offsets': 'offsets', 'word_ids': 'word_ids', 'overflowing': 'overflowing', 'sequence_ids': 'sequence_ids'}, 'input_map': {'sentence': 'sentence', 'sentence_a': 'sentence_a', 'sentence_b': 'sentence_b'}, 'deliver': 'tokenizer', 'process_data': {'is_pretokenized': False}, 'data_type': 'single', 'prefix': ''},
    {'config_path': '*@*', 'prefix': '', 'data_type': 'single', 'process_data': [['source', {'is_pretokenized': False}]], 'post_processor': 'default', 'output_map': {'tokens': 'source_tokens', 'ids': 'source_input_ids', 'attention_mask': 'source_attention_mask', 'type_ids': 'source_type_ids', 'special_tokens_mask': 'source_special_tokens_mask', 'offsets': 'source_offsets', 'word_ids': 'source_word_ids', 'overflowing': 'source_overflowing', 'sequence_ids': 'source_sequence_ids'}, 'deliver': 'source_tokenizer'}.