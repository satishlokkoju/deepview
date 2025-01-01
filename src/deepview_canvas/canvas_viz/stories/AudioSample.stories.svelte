<!-- For licensing see accompanying LICENSE file.
Copyright (C) 2023 betterwithdata Inc. All Rights Reserved. -->

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
  }}
/>

<style global lang="postcss">
  @tailwind base;
  @tailwind components;
  @tailwind utilities;
</style>
