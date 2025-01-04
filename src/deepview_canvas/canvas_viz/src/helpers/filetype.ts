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

import { CanvasDataType } from "../types";

import ImageSample from "../elements/ImageSample.svelte";
import AudioSample from "../elements/AudioSample.svelte";
import TabularSample from "../elements/TabularSample.svelte";

export function getComponentForType(type: CanvasDataType) {
  switch (type) {
    case CanvasDataType.AUDIO:
      return AudioSample;
    case CanvasDataType.IMAGE:
      return ImageSample;
    default:
      return TabularSample;
  }
}
