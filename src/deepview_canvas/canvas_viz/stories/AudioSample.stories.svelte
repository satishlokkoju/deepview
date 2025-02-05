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
  import AudioSample from "../src/elements/AudioSample.svelte";
  import { writable } from "svelte/store";
  import "./utils.css";
  import { CanvasDataType } from "../src/types";
  import audioFile from '../static/canvas-audio-sample.mp3?url';
</script>

<Meta 
  title="AudioSample" 
  component={AudioSample} 
  argTypes={{
    storybook: {
      control: 'boolean',
      description: 'Controls storybook mode',
      defaultValue: true
    },
    large: {
      control: 'boolean',
      description: 'Controls the size of the audio player',
      defaultValue: false
    }
  }} 
/>

<Template let:args>
  <div>
    <AudioSample {...args} />
  </div>
</Template>

<Story
  name="Default"
  args={{
    id: audioFile,
    canvasSpec: writable({
      idColumn: "id",
      filesPath: "",
      dataType: CanvasDataType.AUDIO,
      instancesPerPage: 15,
    }),
    large: true,
    storybook: true
  }}
/>

<style global lang="postcss">
  @tailwind base;
  @tailwind components;
  @tailwind utilities;
</style>
