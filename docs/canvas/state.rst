 .. Copyright 2024 BetterWithData
 
 .. Licensed under the Apache License, Version 2.0 (the "License");
 .. you may not use this file except in compliance with the License.
 .. You may obtain a copy of the License at
 .. 
 ..     http://www.apache.org/licenses/LICENSE-2.0
 .. 
 .. Unless required by applicable law or agreed to in writing, software
 .. distributed under the License is distributed on an "AS IS" BASIS,
 .. WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 .. See the License for the specific language governing permissions and
 .. limitations under the License. 
 

**************
Canvas State
**************

All components have access to the same, shared state.

.. csv-table:: 
   :file: ./state.csv
   :widths: 30, 60, 10
   :header-rows: 1
   :delim: |

If your component has additional requirements, the :code:`WidgetSpec` needs to be changed.
For that, :code:`[your_widget_name]/widget.py` needs to be modified to take additional parameters, for example:

.. code-block:: python

    def __init__(self,
                     width: str = 'XXL',
                     height: str = 'M',
                     page: str = 'Binary Confusion Matrix',
                     label_column: str = '',
                     prediction_column: str = '',
                     **kwargs
                     ):
            """A simple binary confusion matrix extension that takes into account grouping.
    
            Parameters
            ----------
            width : str, optional
                By default "XXL".
            height : str, optional
                By default "M".
            page : str, optional
                Which page of the dashboard to show the widget on, by default "CanvasBinaryConfusionMatrix".
            label_column: str, optional
                The column with the instance label. By default empty.
            prediction_column: str, optional
                The column with the model's prediction. By default empty.
    
            Returns
            -------
            CanvasBinaryConfusionMatrix
            """
            super().__init__(**kwargs)
            self.width: str = width
            self.height: str = height
            self.page: str = page
            self.spec = canvas_ux.ClassificationSpec(
                width=width,
                height=height,
                page=page,
                label_column=label_column,
                prediction_column=prediction_column,
                name=self.name,
                description=self.description
            )

This component takes 2 additional parameters, namely :code:`label_column` and :code:`prediction_column`.
To support typing for this new spec, both the main Canvas :code:`_specs.py` and Canvas Lib's :code:`types.ts` need to be augmented.
