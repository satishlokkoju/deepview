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

<script context="module">
  import SubHeading from "../src/elements/SubHeading.svelte";
  import "./utils.css";
  export const meta = {
    title: "AppHeading",
    component: SubHeading,
    argTypes: {
      heading: { control: "DeepView Heading" },
    },
  };
</script>

<script>
  import { Template, Story } from "@storybook/addon-svelte-csf";
</script>


<Template let:args>
  <SubHeading {...args} />
</Template>

<Story
  name="Default"
  args={{
    heading: "DeepView Test",
  }}
/>

<style global lang="postcss">
  @tailwind base;
  @tailwind components;
  @tailwind utilities;
</style>
