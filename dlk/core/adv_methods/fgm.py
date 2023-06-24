# Copyright cstsunfu. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import torch.nn as nn
import torch
import numpy as np
import random
import re
from . import AdvMethod
from typing import Dict, List
from dlk.utils.logger import Logger
from dlk import register, config_register
from dlk.utils.config import define, float_check, int_check, str_check, options, suggestions, nest_converter
from dlk.utils.config import BaseConfig, IntField, BoolField, FloatField, StrField, NameField, AnyField, NestField, DictField, SubModules

logger = Logger.get_logger()

@config_register("adv_method", 'fgm')
@define
class FGMAdvMethodConfig(BaseConfig):
    name = NameField(value="fgm", file=__file__, help="the adversarial training method")
    @define
    class Config:
        embedding_pattern = StrField(value="model.*embedding.*embedding", help="FGM effect on embedding pattern")
        epsilon = FloatField(value=1.0, checker=float_check(lower=0.0), help="FGM epsilon")
    config = NestField(value=Config, converter=nest_converter)

@register("adv_method", 'fgm')
class FGMAdvMethod(AdvMethod):
    """FGM adversarial training method
    """
    def __init__(self, model: nn.Module, config: FGMAdvMethodConfig):
        super().__init__(model, config)
        self.model = model
        self.config = config.config
        self.backup = {}
        self.adv_para_name = set()
        for name, param in self.model.named_parameters():
            if param.requires_grad and re.findall(self.config.embedding_pattern, name):
                self.adv_para_name.add(name)
        logger.info(f"There are {len(self.adv_para_name)} paras will be adversarial training.")
        logger.info(f"They are {self.adv_para_name}.")

    def attack(self):
        for name, param in self.model.named_parameters():
            if param.requires_grad and name in self.adv_para_name:
                self.backup[name] = param.data.clone()
                norm = torch.norm(param.grad)
                if norm != 0:
                    r_at = self.config.epsilon * param.grad / norm
                    param.data.add_(r_at)

    def restore(self):
        for name, param in self.model.named_parameters():
            if param.requires_grad and name in self.adv_para_name:
                assert name in self.backup
                param.data = self.backup[name]
        self.backup = {}

    def training_step(self, imodel, batch: Dict[str, torch.Tensor], batch_idx: int):
        """do training_step on a mini batch

        Args:
            imodel: imodel instance
            batch: a mini batch inputs
            batch_idx: the index(dataloader) of the mini batch

        Returns: 
            the outputs

        """
        optimizer = imodel.optimizers()
        rt_config={
            "current_step": imodel.global_step,
            "current_epoch": imodel.current_epoch,
            "total_steps": imodel.num_training_steps,
            "total_epochs": imodel.num_training_epochs
        }
        optimizer.zero_grad()
        seed = random.randint(0, int(4e9)) # 4e9 < 2e32 - 1
        torch.manual_seed(seed) # NOTE: should fix manual seed for every forward
        np.random.seed(seed)
        result = imodel.model.training_step(batch)
        loss, _ = imodel.calc_loss(result, batch, rt_config=rt_config)
        imodel.manual_backward(loss)
        self.attack()
        result = imodel.model.training_step(batch)
        loss, loss_log = imodel.calc_loss(result, batch, rt_config=rt_config)
        imodel.manual_backward(loss)
        self.restore()
        optimizer.step()

        schedule = imodel.lr_schedulers()
        schedule.step()
        return loss, loss_log
