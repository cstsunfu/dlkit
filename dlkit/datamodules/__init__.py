"""datamodules"""

import importlib
import os
from typing import Callable, Dict, Type
from dlkit.utils.config import Config
from dlkit.utils.register import Register
from pytorch_lightning import LightningDataModule
import abc

datamodule_config_register = Register("Datamodule config register")
datamodule_register = Register("Datamodule register")

class IDataModule(metaclass=abc.ABCMeta):
    """docstring for ModuleStepMixin"""


    @abc.abstractmethod
    def train_dataloader(self):
        pass

    @abc.abstractmethod
    def predict_dataloader(self):
        pass

    @abc.abstractmethod
    def val_dataloader(self):
        pass

    @abc.abstractmethod
    def test_dataloader(self):
        pass

    @abc.abstractmethod
    def online_dataloader(self):
        pass


class IBaseDataModule(LightningDataModule, IDataModule):
    """docstring for IBaseDataModule"""
    def __init__(self):
        super(IBaseDataModule, self).__init__()
        

def import_datamodules(datamodules_dir, namespace):
    for file in os.listdir(datamodules_dir):
        path = os.path.join(datamodules_dir, file)
        if (
            not file.startswith("_")
            and not file.startswith(".")
            and (file.endswith(".py") or os.path.isdir(path))
        ):
            datamodule_name = file[: file.find(".py")] if file.endswith(".py") else file
            importlib.import_module(namespace + "." + datamodule_name)


# automatically import any Python files in the models directory
datamodules_dir = os.path.dirname(__file__)
import_datamodules(datamodules_dir, "dlkit.datamodules")