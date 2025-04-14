#
#
# Copyright 2024 BetterWithData
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
#
# This file contains code that is part of Apple's DNIKit project, licensed
# under the Apache License, Version 2.0:
#
# Copyright 2022 Apple Inc.
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
#

import typing as t

import tensorflow as tf

from deepview.base import Model
import deepview.typing as dt

# Using type ignores here because the signature of these functions changes (input param)
from ._tf2_loading import load_tf_2_model_from_memory as tf_memory_load  # type: ignore
from ._tf2_loading import load_tf_2_model_from_path as tf_path_load  # type: ignore


def load_tf_model_from_memory(*, model: t.Optional[tf.keras.models.Model] = None) -> Model:
    """
    Initialize a TensorFlow :class:`Model <deepview.base.Model>` from a model loaded in ``memory``.
    This function is supported for TF2, but different parameters are required.
    For TF2, only pass parameter ``model``.

    Args:
        model: Pass only this parameter when running TensorFlow 2. This is the TF Keras model.

    Returns:
        A TensorFlow :class:`Model <deepview.base.Model>`.
    """
    if model is None:
        raise ValueError('For TF2 (currently installed), please pass param `model`')
    return tf_memory_load(model)


def load_tf_model_from_path(path: dt.PathOrStr) -> Model:
    """
    Initialize a TensorFlow :class:`Model <deepview.base.Model>` from a model serialized in ``path``

    Currently accepted serialized model formats, depending on if TF 1 or TF 2 is running.

    TF2 Supported formats:
        - TensorFlow Keras
        - Keras whole models (h5)
        - Keras models with separate architecture and weights files

    Note:
        The keras loaders are currently using ``tf.keras`` instead of ``keras`` natively, and so
        issues might appear when trying to load models saved with native ``keras`` (not tf.keras).
        In this case, load the model outside of DeepView with ``keras`` and pass it to load with
        :func:`load_tf_model_from_memory <deepview_tensorflow.load_tf_model_from_memory>`.

    Args:
        path: Model path (for single model file) or directory that contains all the model files.

    Returns:
        A DeepView TensorFlow :class:`Model <deepview.base.Model>`.
    """
    return tf_path_load(path)
