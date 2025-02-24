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

import {
  DOMWidgetModel,
  ISerializers,
} from '@jupyter-widgets/base';

import { MODULE_NAME, MODULE_VERSION } from './version';

import { CanvasBaseDomWidgetView } from '@betterwithdata/canvas_viz';

import Toolbar from './toolbar/Toolbar.svelte';

export class ToolbarModel extends DOMWidgetModel {
  defaults() {
    return {
      ...super.defaults(),
      _model_name: ToolbarModel.model_name,
      _model_module: ToolbarModel.model_module,
      _model_module_version: ToolbarModel.model_module_version,
      _view_name: ToolbarModel.view_name,
      _view_module: ToolbarModel.view_module,
      _view_module_version: ToolbarModel.view_module_version,
    };
  }

  static serializers: ISerializers = {
    ...DOMWidgetModel.serializers,
    // Add any extra serializers here
  };

  static model_name = 'ToolbarModel';
  static model_module = MODULE_NAME;
  static model_module_version = MODULE_VERSION;
  static view_name = 'ToolbarView'; // Set to null if no view
  static view_module = MODULE_NAME; // Set to null if no view
  static view_module_version = MODULE_VERSION;
}

export class ToolbarView extends CanvasBaseDomWidgetView {
  render() {
    this.setupWidget(this.model, Toolbar);
  }
}

