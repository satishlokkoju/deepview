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
  import Dropdown from "../src/elements/Dropdown.svelte";
  import "./utils.css";
</script>

<Meta
  title="Dropdown"
  component={Dropdown}
  argTypes={{
    value: {
      control: { type: "select", options: ["value1", "value2", "value3"] },
    },
  }}
/>

<Template let:args>
  <Dropdown {...args} />
</Template>

<Story
  name="Default"
  args={{
    value: "value1",
    items: ["value1", "value2", "value3"],
  }}
/>

<style global lang="postcss">
  @tailwind base;
  @tailwind components;
  @tailwind utilities;
</style>
