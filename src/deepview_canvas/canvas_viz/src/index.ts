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


import { DOMWidgetModel, ISerializers } from "@jupyter-widgets/base";
export * from "./types";
export * from "./elements";
export * from "./helpers";
export * from "./stores";
export * from "./canvasbasewidget";
export { default as JupyterWidget } from "./JupyterWidget.svelte";

export const serializers: ISerializers = {
  ...DOMWidgetModel.serializers,
  table: {
    serialize: (value: any): DataView => {
      return new DataView(value.buffer.slice(0));
    },
  },
};
