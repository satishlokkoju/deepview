// For licensing see accompanying LICENSE file.
// Copyright (C) 2023 betterwithdata Inc. All Rights Reserved.

import { MODULE_NAME, MODULE_VERSION } from './version';
import {
  DOMWidgetModel,
  DOMWidgetView,
  ISerializers,
} from '@jupyter-widgets/base';

import {serializers, JupyterWidget } from '@betterwithdata/canvas_viz';

import CanvasScatterplot from './CanvasScatterplot.svelte';

export class CanvasScatterplotModel extends DOMWidgetModel {
  defaults() {
    return {
      ...super.defaults(),
      _model_name: CanvasScatterplotModel.model_name,
      _model_module: CanvasScatterplotModel.model_module,
      _model_module_version: CanvasScatterplotModel.model_module_version,
      _view_name: CanvasScatterplotModel.view_name,
      _view_module: CanvasScatterplotModel.view_module,
      _view_module_version: CanvasScatterplotModel.view_module_version,
    };
  }
  static serializers: ISerializers = serializers;

  static model_name = 'CanvasScatterplotModel';
  static model_module = MODULE_NAME;
  static model_module_version = MODULE_VERSION;
  static view_name = 'CanvasScatterplotView'; // Set to null if no view
  static view_module = MODULE_NAME; // Set to null if no view
  static view_module_version = MODULE_VERSION;
}

export class CanvasScatterplotView extends DOMWidgetView {
  render() {
    new JupyterWidget({
      target: this.el,
      props: {
        model: this.model,
        widget: CanvasScatterplot,
      },
    });
  }
}
