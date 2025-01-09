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
  import SampleRowContainer from "../src/elements/SampleRowContainer.svelte";
  import { writable } from "svelte/store";
  import "./utils.css";
  import { CanvasDataType } from "../src/types";
  import AudioSample from "../static/canvas-audio-sample.mp3"
</script>

<Meta
  title="SampleRowContainer"
  component={SampleRowContainer}
  argTypes={{
    type: {
      control: { type: "select", options: ["image", "audio", "tabular"] },
    },
  }}
/>

<Template let:args>
  <SampleRowContainer
    dataPoints={args.dataPoints[args.type]}
    selected={args.selected}
    canvasSpec={args.specs[args.type]}
    tooltip={args.tooltips[args.type]}
    storybook={true}
  />
</Template>

<Story
  name="Default"
  args={{
    type: "image",
    dataPoints: {
      image: [
        {
          id: "/200?random=1",
        },
        {
          id: "/200?random=2",
        },
        {
          id: "/200?random=3",
        },
        {
          id: "/200?random=4",
        },
        {
          id: "/200?random=5",
        },
        {
          id: "/200?random=6",
        },
        {
          id: "/200?random=7",
        },
        {
          id: "/200?random=8",
        },
        {
          id: "/200?random=9",
        },
        {
          id: "/200?random=10",
        }
      ],
      audio: [
        {
          id: AudioSample
        },
        {
          id: AudioSample
        },
        {
          id: AudioSample
        },
      ],
      tabular: [
        { id: "row1" },
        { id: "row2" },
        { id: "row3" },
        { id: "row4" },
        { id: "row5" },
        { id: "row6" },
        { id: "row7" },
      ],
    },
    selected: writable([]),
    specs: {
      image: writable({
        idColumn: "id",
        dataType: CanvasDataType.IMAGE,
        filesPath:
          "https://picsum.photos/",
      }),
      audio: writable({
        idColumn: "id",
        dataType: CanvasDataType.AUDIO,
        filesPath: "",
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
        fetchPrefix:
          "https://picsum.photos/",
        number: 100,
        instance: {
          id: "/200?random=1",
        },
      }),
      audio: writable({
        hover: true,
        mousePos: { x: 0, y: 0 },
        filesPath: "",
        number: 100,
        instance: {
          id: AudioSample
        },
      }),
      tabular: writable({
        hover: true,
        mousePos: { x: 0, y: 0 },
        number: 100,
        instance: {
          id: "row1",
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
