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

<script lang="ts">
  import type { ColumnTable } from 'arquero';
  import type {
    SummaryElement,
    ChartData,
    CanvasSpec,
  } from '@betterwithdata/canvas_viz';

  import { CanvasVegaLite, TextField } from '@betterwithdata/canvas_viz';
  import { createEventDispatcher } from 'svelte';

  export let canvasSpec: CanvasSpec;
  export let element: SummaryElement;
  export let table: ColumnTable;
  export let filteredTable: ColumnTable;
  export let editMode: boolean = false;

  let value = '';
  const dispatch = createEventDispatcher();

  $: typedData = element.data as ChartData;
  $: title = typedData.spec.title === undefined ? '' : typedData.spec.title;
  $: value = title as string;
  $: {
    if (value !== typedData.spec.title) {
      dispatch('update', {
        element: {
          ...element,
          data: { ...typedData, spec: { ...typedData.spec, title: value } },
        },
        oldElement: element,
      });
    }
  }
</script>

<div
  class="{editMode
    ? 'border border-button_outline'
    : ''} rounded m-1 flex flex-col"
>
  {#if editMode}
    <div class="flex m-1">
      <div class="flex-grow">
        <TextField bind:value placeholder="Chart Title" />
      </div>
    </div>
  {/if}
  <CanvasVegaLite
    data={typedData.data}
    spec={typedData.spec}
    resolver={typedData.resolver}
    {table}
    {filteredTable}
    showUnfilteredData={canvasSpec.showUnfilteredData}
  />
</div>
