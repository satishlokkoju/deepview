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
  import TabularSample from "../src/elements/TabularSample.svelte";
  import "./utils.css";

  const sampleData = [
    { id: 1, name: "Sample 1", value: 42, category: "A" },
    { id: 2, name: "Sample 2", value: 28, category: "B" },
    { id: 3, name: "Sample 3", value: 35, category: "A" },
    { id: 4, name: "Sample 4", value: 51, category: "C" },
    { id: 5, name: "Sample 5", value: 19, category: "B" },
  ];
</script>

<Meta 
  title="TabularSample" 
  component={TabularSample} 
  argTypes={{
    data: { control: 'object' },
    maxRows: { control: 'number' },
    storybook: { control: 'boolean' }
  }} 
/>

<Template let:args>
  <div class="p-4 bg-white">
    <TabularSample {...args} />
  </div>
</Template>

<Story 
  name="Empty" 
  args={{
    data: [],
    maxRows: 10,
    storybook: true
  }} 
/>

<Story 
  name="With Data" 
  args={{
    data: sampleData,
    maxRows: 10,
    storybook: true
  }} 
/>

<Story 
  name="Limited Rows" 
  args={{
    data: sampleData,
    maxRows: 3,
    storybook: true
  }} 
/>

<style global lang="postcss">
  @tailwind base;
  @tailwind components;
  @tailwind utilities;
</style>
