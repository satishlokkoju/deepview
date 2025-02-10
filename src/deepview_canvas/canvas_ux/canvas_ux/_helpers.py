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

"""Helper functions for creating Canvas widgets"""
from __future__ import absolute_import

import re
from dataclasses import asdict, is_dataclass
from pathlib import Path

import pandas as pd
import pyarrow as pa
from traitlets import TraitType
from typing import Optional, Union, Any

from ._specs import CanvasDataType


def to_arrow_file(table: Union[pa.Table, pd.DataFrame], export_path: Union[str, Path]) -> None:
    """Save a PyArrow or Pandas table as a .arrow file.
    Parameters
    ----------
    table : pa.Table or pd.DataFrame
        A Pandas DataFrame, Apache Arrow table with metadata columns.
    export_path : Union[str,Path]
        Where to save the file to.
    """
    export_path = Path(export_path)
    if isinstance(table, pd.DataFrame):
        table = pa.Table.from_pandas(table)
    table_to_file(table, Path(export_path, 'table.arrow'))


def table_to_file(table: pa.Table, path: Union[str, Path]) -> None:
    sink = path
    writer = pa.ipc.new_file(sink, table.schema)
    writer.write(table)
    writer.close()


def serialize_table(table: pa.Table) -> bytes:
    sink = pa.BufferOutputStream()
    writer = pa.RecordBatchStreamWriter(sink, table.schema)
    writer.write_table(table)
    writer.close()
    return sink.getvalue().to_pybytes()


def deserialize_table(data: bytes) -> pa.Table:
    reader = pa.RecordBatchStreamReader(data)
    table = reader.read_all()
    return table


def get_data_type(type: Optional[CanvasDataType], id: str) -> CanvasDataType:
    if type:
        return type

    if id[-3:] == 'wav':
        return CanvasDataType.AUDIO
    elif id[-3:] == 'png' or id[-3:] == 'jpg' or id[-3:] == 'bmp' or id[-4:] == 'jpeg' or id[-3:] == 'tif' or id[-4:] == 'tiff':
        return CanvasDataType.IMAGE
    else:
        return CanvasDataType.TABULAR


def get_num_instances_by_data_type(instancesPerPage: Optional[int], type: CanvasDataType) -> int:
    if instancesPerPage:
        return instancesPerPage

    if type == CanvasDataType.AUDIO:
        return 20
    elif type == CanvasDataType.IMAGE:
        return 40
    else:
        return 150


def dataclass_to_camel_dict(spec: Any) -> dict:
    """Convert dataclass to camelCase dictionary

    Args:
        spec: A dataclass instance

    Returns:
        A dictionary representation of the dataclass instance
    Raises:
        TypeError: If spec is not a dataclass instance
    """
    if not is_dataclass(spec):
        raise TypeError("Input must be a dataclass instance")
    spec_dict = asdict(spec)  # type: ignore
    new_dict = {}
    for key in spec_dict:
        new_key = ''.join([word.title() for word in key.split('_')])
        new_key = new_key[0].lower() + new_key[1:]
        new_dict[new_key] = spec_dict[key]
    return new_dict


def camel_dict_to_snake_case_dict(spec_dict: dict) -> dict:
    new_dict = {}
    for key in spec_dict:
        new_key = re.sub(r'(?<!^)(?=[A-Z])', '_', key).lower()
        new_dict[new_key] = spec_dict[key]
    return new_dict


class ByteMemoryView(TraitType):
    """A trait for memory views of bytes."""

    default_value = memoryview(b'')
    info_text = 'a memory view object'

    def validate(self, obj, value: memoryview) -> memoryview:  # type: ignore
        if isinstance(value, memoryview) and value.format == 'B':
            return value
        self.error(obj, value)  # type: ignore

    def default_value_repr(self) -> str:
        return repr(self.default_value.tobytes())


class CByteMemoryView(ByteMemoryView):
    """A casting version of the byte memory view trait."""

    def validate(self, obj, value: memoryview) -> memoryview:  # type: ignore
        if isinstance(value, memoryview) and value.format == 'B':
            return value

        try:
            mv = memoryview(value)
            if mv.format != 'B':
                mv = mv.cast('B')
            return mv
        except Exception:
            self.error(obj, value)  # type: ignore
