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
    TooltipSpec,
    CanvasSpec,
  } from '@betterwithdata/canvas_viz';
  import type { ColumnTable } from 'arquero';
  import type { Writable } from 'svelte/store';

  import { mapHeight, Pagination, ComponentHeader } from '@betterwithdata/canvas_viz';

  export let widgetSpec: WidgetSpec;
  export let fullSize: boolean = false;
  export let filteredTable: Writable<ColumnTable>;
  export let groupedTables: Writable<ColumnTable[]>;
  export let groupNames: Writable<string[][]>;
  export let selected: Writable<string[]>;
  export let tooltip: Writable<TooltipSpec>;
  export let storybook: boolean = false;
  export let canvasSpec: Writable<CanvasSpec>;

  let container: HTMLDivElement;
</script>

<div
  class="flex flex-col p-2 {fullSize ? 'h-full' : mapHeight(widgetSpec.height)}"
>
  <ComponentHeader
    title={'Data Explorer'}
    description={widgetSpec.description}
    {container}
  />
  <div
    class="flex flex-col justify-between overflow-hidden flex-grow"
    bind:this={container}
  >
    {#if $groupNames.length === 0}
      <Pagination
        title="Instance List"
        filteredTable={$filteredTable}
        {selected}
        {tooltip}
        {canvasSpec}
        {storybook}
      />
    {:else}
      <div class="flex flex-col overflow-auto">
        {#each $groupedTables as table, i}
          {#if table.size !== 0}
            <div class="mt-2">
              <Pagination
                title={$groupNames[i].join(' | ')}
                filteredTable={table}
                {selected}
                {tooltip}
                {canvasSpec}
                {storybook}
              />
            </div>
          {/if}
        {/each}
      </div>
    {/if}
  </div>
</div>
