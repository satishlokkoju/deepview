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
  import HeaderButton from "../src/elements/HeaderButton.svelte";
  import "./utils.css";
</script>

<Meta
  title="HeaderButton"
  component={HeaderButton}
  argTypes={{
    value: { control: "text" },
    selected: { control: "boolean" },
  }}
/>

This is meant to be rendered on black background. Thus, we put it in a black div
with padding.
<br />
<div class="p-4 bg-black">
  <Template let:args>
    <HeaderButton {...args} />
  </Template>
</div>

<Story
  name="Default"
  args={{
    selected: false,
    value: "test",
  }}
/>

<style global lang="postcss">
  @tailwind base;
  @tailwind components;
  @tailwind utilities;
</style>
