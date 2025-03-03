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
  import type {
    WidgetSpec,
    CanvasSpec,
    TooltipSpec,
  } from '@betterwithdata/canvas_viz';
  import type { ColumnTable } from 'arquero';
  import type { Writable } from 'svelte/store';

  import DuplicatesList from './DuplicatesList.svelte';
  import { mapHeight, Dropdown, ComponentHeader } from '@betterwithdata/canvas_viz';

  export let widgetSpec: WidgetSpec;
  export let fullSize = false;
  export let filteredTable: Writable<ColumnTable>;
  export let canvasSpec: Writable<CanvasSpec>;
  export let groupColumns: Writable<string[]>;
  export let groupNames: Writable<string[][]>;
  export let selected: Writable<string[]>;
  export let tooltip: Writable<TooltipSpec>;
  export let storybook = false;

  let selectedLayer: string;
  let container: HTMLDivElement;

  $: columnNames = $filteredTable.columnNames((d) =>
    d.startsWith('duplicates_')
  );
  $: layerNames = columnNames.map((name) => name.substring(11));
  $: if (selectedLayer === undefined)
    {selectedLayer = layerNames[0] !== undefined ? layerNames[0] : '';}
  $: selectedColumn =
    selectedLayer === undefined
      ? ''
      : columnNames.find((name) => name.includes(selectedLayer));
</script>

<div
  class="flex flex-col overflow-hidden p-2 {fullSize
    ? 'h-full'
    : mapHeight(widgetSpec.height)}"
>
  <ComponentHeader
    title={'Duplicates'}
    description={widgetSpec.description}
    {container}
  >
    {#if layerNames.length > 1}
      <div class="mr-4 flex flex-row mb-2 items-center">
        <p class="mr-2">Layer:</p>
        <Dropdown bind:value={selectedLayer} items={layerNames} />
      </div>
    {/if}
  </ComponentHeader>
  <div bind:this={container} class="flex flex-col min-h-0 flex-1">
    {#if layerNames[0] !== undefined}
      {#if selectedColumn !== ''}
        <DuplicatesList
          selectedColumn={selectedColumn}
          filteredTable={filteredTable}
          canvasSpec={canvasSpec}
          groupColumns={groupColumns}
          groupNames={groupNames}
          selected={selected}
          tooltip={tooltip}
          storybook={storybook}
        />
      {/if}
    {:else}
      <p>
        No duplicate columns found. A duplicate column must start with
        'duplicates_'
      </p>
    {/if}
  </div>
</div>
