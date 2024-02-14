# Copyright the author(s) of DLK.
#
# This source code is licensed under the Apache license found in the
# LICENSE file in the root directory of this source tree.

from typing import Dict

import torch
import torch.nn as nn
from intc import (
    MISSING,
    AnyField,
    Base,
    BoolField,
    DictField,
    FloatField,
    IntField,
    ListField,
    NestField,
    StrField,
    SubModule,
    cregister,
)

from dlk.utils.register import register

from . import BaseLoss, BaseLossConfig


@cregister("loss", "bce")
class BCEWithLogitsLossConfig(BaseLossConfig):
    """the binary crossentropy loss"""


@register("loss", "bce")
class BCEWithLogitsLoss(BaseLoss):
    """binary crossentropy for bi-class classification"""

    def __init__(self, config: BCEWithLogitsLossConfig):
        super(BCEWithLogitsLoss, self).__init__(config)
        self.bce = nn.BCEWithLogitsLoss(reduction=self.config.reduction)

    def _calc(self, result, inputs, rt_config, scale):
        """calc the loss the predict is from result, the ground truth is from inputs

        Args:
            result: the model predict dict
            inputs: the all inputs for model
            rt_config: provide the current training status
                >>> {
                >>>     "current_step": self.global_step,
                >>>     "current_epoch": self.current_epoch,
                >>>     "total_steps": self.num_training_steps,
                >>>     "total_epochs": self.num_training_epochs
                >>> }
            scale: the scale rate for the loss

        Returns:
            loss

        """
        pred = result[self.pred_name]
        target = inputs[self.truth_name]
        loss = self.bce(torch.sigmoid(pred), target) * scale
        return loss, {self.config.log_map.loss: loss}
