import hjson
import os
from typing import Dict, Union, Callable, List, Any
from dlkit.utils.parser import BaseConfigParser
from dlkit.utils.config import ConfigTool
from dlkit.data.datamodules import datamodule_register, datamodule_config_register
from dlkit.managers import manager_register, manager_config_register
from dlkit.core.imodels import imodel_register, imodel_config_register
import pickle as pkl
import torch
import uuid
import json
from dlkit.utils.logger import logger

logger = logger()


class Predict(object):
    """docstring for Trainer
        {
            "_focus": {

            },
            "_link": {},
            "_search": {},
            "config": {
                "save_dir": "*@*",  # must be provided
                "data_path": "*@*",  # must be provided
            },
            "task": {
                "_name": task_name
                ...
            }
        }
    """
    def __init__(self, config, checkpoint):
        super(Predict, self).__init__()
        if not isinstance(config, dict):
            config = hjson.load(open(config), object_pairs_hook=dict)

        self.focus = config.pop('_focus', {})
        self.config = config
        # self.configs = config_parser_register.get('root')(config).parser_with_check()
        self.configs = BaseConfigParser(config).parser_with_check()
        self.ckpt = torch.load(checkpoint)
        config_name = []
        for source, to in self.focus.items():
            config_point = config
            trace = source.split('.')
            for t in trace:
                config_point = config_point[t]
            config_name.append(to+str(config_point))
        if config_name:
            name_str = '_'.join(config_name)
        else:
            name_str = config['_name']
        self.name_str = name_str

    def dump_config(self, config, name):
        """TODO: Docstring for dump_config.

        :config: TODO
        :returns: TODO

        """
        log_path = os.path.join(config.get('config').get('save_dir'), name)
        os.makedirs(log_path, exist_ok=True)
        json.dump({"root":config, "_focus": self.focus}, open(os.path.join(config.get('config').get('save_dir'), name, "config.json"), 'w'), ensure_ascii=False, indent=4)

    def predict(self):
        """TODO: Docstring for run_oneturn.
        """

        config = self.config['root']
        name = self.name_str
        # get data
        data = self.get_data(config)

        # set datamodule
        datamodule = self.get_datamodule(config, data)

        # set training manager
        manager = self.get_manager(config, name)

        # init imodel and inject the origin test and valid data
        imodel = self.get_imodel(config, data)

        # start training
        predict_result = manager.predict(model=imodel, datamodule=datamodule)
        imodel.postprocessor(stage='predict', list_batch_outputs=predict_result, origin_data=data['predict'], rt_config={}),

    def get_data(self, config):
        """TODO: Docstring for get_data.
        :returns: TODO

        """
        self.data = pkl.load(open(config['config']['data_path'], 'rb')).get('data', {})
        return self.data

    def get_datamodule(self, config, data):
        """TODO: Docstring for get_datamodule.

        :config: TODO
        :returns: TODO

        """
        DataModule, DataModuleConfig = ConfigTool.get_leaf_module(datamodule_register, datamodule_config_register, 'datamodule', config['task']['datamodule'])
        datamodule = DataModule(DataModuleConfig, data)
        return datamodule
        
    def get_manager(self, config, name):
        """TODO: Docstring for get_manager.

        :config: TODO
        :returns: TODO

        """
        Manager, ManagerConfig = ConfigTool.get_leaf_module(manager_register, manager_config_register, 'manager', config.get('task').get('manager'))
        manager = Manager(ManagerConfig, rt_config={"save_dir": config.get('config').get("save_dir"), "name": name})
        return manager

    def get_imodel(self, config, data):
        """TODO: Docstring for get_imodel.

        :config: TODO
        :returns: TODO

        """
        IModel, IModelConfig = ConfigTool.get_leaf_module(imodel_register, imodel_config_register, 'imodel', config.get('task').get('imodel'))
        imodel = IModel(IModelConfig)
        imodel.load_state_dict(self.ckpt['state_dict'])
        return imodel
