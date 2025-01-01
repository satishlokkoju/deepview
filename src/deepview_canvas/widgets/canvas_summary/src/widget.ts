// For licensing see accompanying LICENSE file.
// Copyright (C) 2023 betterwithdata Inc. All Rights Reserved.

import { MODULE_NAME, MODULE_VERSION } from './version';
import {
  DOMWidgetModel,
  DOMWidgetView,
  ISerializers,
} from '@jupyter-widgets/base';

import {serializers, JupyterWidget } from '@betterwithdata/canvas_viz';

import CanvasSummary from './CanvasSummary.svelte';

export class CanvasSummaryModel extends DOMWidgetModel {
  defaults() {
    return {
      ...super.defaults(),
      _model_name: CanvasSummaryModel.model_name,
      _model_module: CanvasSummaryModel.model_module,
      _model_module_version: CanvasSummaryModel.model_module_version,
      _view_name: CanvasSummaryModel.view_name,
      _view_module: CanvasSummaryModel.view_module,
      _view_module_version: CanvasSummaryModel.view_module_version,
    };
  }
  static serializers: ISerializers = serializers;

  static model_name = 'CanvasSummaryModel';
  static model_module = MODULE_NAME;
  static model_module_version = MODULE_VERSION;
  static view_name = 'CanvasSummaryView'; // Set to null if no view
  static view_module = MODULE_NAME; // Set to null if no view
  static view_module_version = MODULE_VERSION;
}

export class CanvasSummaryView extends DOMWidgetView {
  render() {
    new JupyterWidget({
      target: this.el,
      props: {
        model: this.model,
        widget: CanvasSummary,
      },
    });
  }
}
