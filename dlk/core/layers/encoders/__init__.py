# Copyright 2021 cstsunfu. All rights reserved.
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

"""encoders"""

import importlib
import os
from dlk.utils.register import Register


encoder_config_register = Register("Encoder config register.")
encoder_register = Register("Encoder register.")

def import_encoders(encoders_dir, namespace):
    for file in os.listdir(encoders_dir):
        path = os.path.join(encoders_dir, file)
        if (
            not file.startswith("_")
            and not file.startswith(".")
            and (file.endswith(".py") or os.path.isdir(path))
        ):
            encoder_name = file[: file.find(".py")] if file.endswith(".py") else file
            importlib.import_module(namespace + "." + encoder_name)



# automatically import any Python files in the encoders directory
encoders_dir = os.path.dirname(__file__)
import_encoders(encoders_dir, "dlk.core.layers.encoders")
