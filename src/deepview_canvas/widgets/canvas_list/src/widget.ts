/**
 * Copyright 2024 BetterWithData
 * 
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 * 
 *     http://www.apache.org/licenses/LICENSE-2.0
 * 
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License. 
 */

import { MODULE_NAME, MODULE_VERSION } from './version';
import {
  DOMWidgetModel,
  ISerializers,
} from '@jupyter-widgets/base';

import {serializers, CanvasBaseDomWidgetView } from '@betterwithdata/canvas_viz';

import CanvasList from './CanvasList.svelte';

export class CanvasListModel extends DOMWidgetModel {
  defaults() {
    return {
      ...super.defaults(),
      _model_name: CanvasListModel.model_name,
      _model_module: CanvasListModel.model_module,
      _model_module_version: CanvasListModel.model_module_version,
      _view_name: CanvasListModel.view_name,
      _view_module: CanvasListModel.view_module,
      _view_module_version: CanvasListModel.view_module_version,
    };
  }
  static serializers: ISerializers = serializers;

  static model_name = 'CanvasListModel';
  static model_module = MODULE_NAME;
  static model_module_version = MODULE_VERSION;
  static view_name = 'CanvasListView'; // Set to null if no view
  static view_module = MODULE_NAME; // Set to null if no view
  static view_module_version = MODULE_VERSION;
}

export class CanvasListView extends CanvasBaseDomWidgetView {
  render() {
    this.setupWidget(this.model, CanvasList);
  }
}
