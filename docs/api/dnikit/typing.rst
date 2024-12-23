======
Typing
======

This module contains all DeepView custom types.

.. automodule:: deepview.typing
    :members:
    :undoc-members:
    :show-inheritance:

.. py:data:: deepview.typing.OneOrMany

alias of Union[_T, Collection[_T]]

.. py:data:: deepview.typing.OneManyOrNone

alias of Union[None, _T, Collection[_T]]

.. py:data:: deepview.typing.PathOrStr

alias of Union[str, pathlib.Path]

.. py:data:: deepview.typing.StringLike

alias of Any.
Similar to "array like" -- these are types that can be losslessly converted
to/from string and they might be used as Identifiers in a Batch.
