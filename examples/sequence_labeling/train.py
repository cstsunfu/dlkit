# Copyright the author(s) of DLK.
#
# This source code is licensed under the Apache license found in the
# LICENSE file in the root directory of this source tree.

import json

import lightning as pl
from intc import ic_repo

from dlk.train import Train

pl.seed_everything(88)

trainer = Train("./config/bert_firstpiece_lstm_crf/fit.jsonc")
trainer.run()
