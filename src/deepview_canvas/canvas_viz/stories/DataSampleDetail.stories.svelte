<!-- # Copyright 2024 BetterWithData
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License. -->

<script>
  import { Meta, Template, Story } from "@storybook/addon-svelte-csf";
  import DataSampleDetail from "../src/elements/DataSampleDetail.svelte";
  import "./utils.css";
  import { CanvasDataType } from "../src/types";
  import AudioSample from "../static/canvas-audio-sample.mp3";
  import { writable } from "svelte/store";
</script>

<Meta
  title="DataSampleDetail"
  component={DataSampleDetail}
  argTypes={{
    type: {
      control: "select",
      options: ["image", "audio", "tabular"],
      defaultValue: "image",
      description: "Type of data sample to display"
    }
  }}
/>



<Template let:args>
  <DataSampleDetail
    canvasSpec={args.specs[args.type]}
    tooltip={args.tooltips[args.type]}
    storybook={true}
  />
</Template>

<Story
  name="Default"
  args={{
    type: "image",
    specs: {
      image: writable({
        idColumn: "id",
        filesPath:
          "https://picsum.photos/",
        dataType: CanvasDataType.IMAGE,
      }),
      audio: writable({
        idColumn: "id",
        filesPath: "",
        dataType: CanvasDataType.AUDIO,
      }),
      tabular: writable({
        idColumn: "id",
        dataType: CanvasDataType.TABULAR,
      }),
    },
    tooltips: {
      image: writable({
        hover: true,
        mousePos: { x: 0, y: 0 },
        filesPath:
          "https://picsum.photos/",
        number: 941,
        instance: {
          id: "/200?random=1",
          foo: "test",
          bar: "test",
          numbervalue: 941,
          list: [9,4,1],
        },
      }),
      audio: writable({
        hover: true,
        mousePos: { x: 0, y: 0 },
        filesPath: "",
        number: 941,
        instance: {
          id: AudioSample,
        },
      }),
      tabular: writable({
        hover: true,
        mousePos: { x: 0, y: 0 },
        number: 941,
        instance: {
          id: "row1",
          foo: "test",
          bar: "test",
          numbervalue: 941,
          list: [9,4,1],
        },
      }),
    },
  }}
/>

<style global lang="postcss">
  @tailwind base;
  @tailwind components;
  @tailwind utilities;
</style>
