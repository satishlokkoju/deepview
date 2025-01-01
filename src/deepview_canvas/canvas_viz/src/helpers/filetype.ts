// For licensing see accompanying LICENSE file.
// Copyright (C) 2023 betterwithdata Inc. All Rights Reserved.

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
