import { DOMWidgetView } from '@jupyter-widgets/base';
import type { DOMWidgetModel } from '@jupyter-widgets/base';
import JupyterWidget from './JupyterWidget.svelte';
import { initializeStores } from './stores';
import type { ComponentType } from "svelte";

export class CanvasBaseDomWidgetView extends DOMWidgetView {
  protected setupWidget(model: DOMWidgetModel, canvasWidget: ComponentType) {
    initializeStores(model);
    
    new JupyterWidget({
      target: this.el,
      props: {
        model: model,
        widget: canvasWidget,
      },
    });
  }

  render() {
    throw new Error('render() must be implemented by Canvas Widget');
  }
}