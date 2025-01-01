// For licensing see accompanying LICENSE file.
// Copyright (C) 2023 betterwithdata Inc. All Rights Reserved.

import { MODULE_NAME, MODULE_VERSION } from './version';
import {
  DOMWidgetModel,
  DOMWidgetView,
  ISerializers,
} from '@jupyter-widgets/base';

import {serializers, JupyterWidget } from '@betterwithdata/canvas_viz';

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

export class CanvasListView extends DOMWidgetView {
  render() {
    new JupyterWidget({
      target: this.el,
      props: {
        model: this.model,
        widget: CanvasList,
      },
    });
  }
}
