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
  import IconButton from "../src/elements/IconButton.svelte";
  import "./utils.css";
</script>

<Meta
  title="IconButton"
  component={IconButton}
  argTypes={{
    filled: { control: "boolean" },
  }}
/>

<Template let:args>
  <IconButton {...args}>
    <div slot="icon">
      <span>An IconButton can hold an icon via a slot named </span>
      <code>icon</code>
      <span>.</span>
    </div>
    <div slot="text">
      <span>And text with a slot named</span>
      <code>text</code>
      <span>.</span>
    </div>
  </IconButton>
  <IconButton {...args}>
    <div slot="icon">
      <span>icon</span>
    </div>
    <div slot="text">
      <span>text</span>
    </div>
  </IconButton>
</Template>

<Story
  name="Default"
  args={{
    filled: false,
  }}
/>

<style global lang="postcss">
  @tailwind base;
  @tailwind components;
  @tailwind utilities;
</style>
