import torch.nn as nn
from . import callback_register, callback_config_register
from pytorch_lightning.callbacks import LearningRateMonitor
        

@callback_config_register('lr_monitor')
class LearningRateMonitorCallbackConfig(object):
    """docstring for LearningRateMonitorCallbackConfig
        {
            "_name": "lr_monitor",
            "config": {
                "logging_interval": null,
                "log_momentum": false,
            }
        }
    """
    def __init__(self, config: Dict):
        config = config['config']
        self.logging_interval = config["logging_interval"]
        self.log_momentum = config["log_momentum"]


@callback_register('lr_monitor')
class LearningRateMonitorCallback(object):
    """
    """

    def __init__(self, config: LearningRateMonitorCallbackConfig):
        super().__init__()
        self.config = config

    def __call__(self, rt_config):
        """TODO: Docstring for __call__.

        :rt_config: Dict: TODO
        :returns: TODO

        """
        return LearningRateMonitor(**self.config.__dict__)
