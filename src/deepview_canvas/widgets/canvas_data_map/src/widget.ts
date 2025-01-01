// For licensing see accompanying LICENSE file.
// Copyright (C) 2023 betterwithdata Inc. All Rights Reserved.

import { MODULE_NAME, MODULE_VERSION } from './version';
import {
  DOMWidgetModel,
  DOMWidgetView,
  ISerializers,
} from '@jupyter-widgets/base';

import { serializers, JupyterWidget } from '@betterwithdata/canvas_viz';

import CanvasDataMap from './CanvasDataMap.svelte';

export class CanvasDataMapModel extends DOMWidgetModel {
  defaults() {
    return {
      ...super.defaults(),
      _model_name: CanvasDataMapModel.model_name,
      _model_module: CanvasDataMapModel.model_module,
      _model_module_version: CanvasDataMapModel.model_module_version,
      _view_name: CanvasDataMapModel.view_name,
      _view_module: CanvasDataMapModel.view_module,
      _view_module_version: CanvasDataMapModel.view_module_version,
    };
  }
  static serializers: ISerializers = serializers;

  static model_name = 'CanvasDataMapModel';
  static model_module = MODULE_NAME;
  static model_module_version = MODULE_VERSION;
  static view_name = 'CanvasDataMapView'; // Set to null if no view
  static view_module = MODULE_NAME; // Set to null if no view
  static view_module_version = MODULE_VERSION;
}

export class CanvasDataMapView extends DOMWidgetView {
  render() {
    new JupyterWidget({
      target: this.el,
      props: {
        model: this.model,
        widget: CanvasDataMap,
      },
    });
  }
}
