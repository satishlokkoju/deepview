<!--
# Copyright 2024 BetterWithData
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
  import type { CanvasSpec, TooltipSpec } from '@betterwithdata/canvas_viz';
  import type { ColumnTable } from 'arquero';
  import type { Writable } from 'svelte/store';

  import { PaginationControls } from '@betterwithdata/canvas_viz';
  import DatasetDuplicatesList from './DatasetDuplicatesList.svelte';

  export let selectedColumn: string;
  export let filteredTable: Writable<ColumnTable>;
  export let canvasSpec: Writable<CanvasSpec>;
  export let groupColumns: Writable<string[]>;
  export let groupNames: Writable<string[][]>;
  export let selected: Writable<string[]>;
  export let tooltip: Writable<TooltipSpec>;
  export let storybook = false;

  const NUMBER_SHOWN = 17;
  $: rowsPerPage = Math.ceil(
    Math.max($canvasSpec.instancesPerPage / NUMBER_SHOWN, 5)
  );

  let groupedDuplicates: Record<string, Record<string, unknown>[]> = {};
  let groupKeys: string[] = [];
  let page = 0;

  filteredTable.subscribe(() => (page = 0));
  groupColumns.subscribe(() => (page = 0));

  $: duplicateRows = $filteredTable
    .filter(`(d) => d["${selectedColumn}"] !== -1`)
    .objects();
  $: {
    groupedDuplicates = {};
    duplicateRows.forEach((row) => {
      const group: number = row[selectedColumn];
      if (groupedDuplicates[group] === undefined) {
        groupedDuplicates[group] = [];
      }
      groupedDuplicates[group].push(row);
    });
    groupKeys = Object.keys(groupedDuplicates);
    groupKeys.sort(
      (a, b) => groupedDuplicates[b].length - groupedDuplicates[a].length
    );
  }
</script>

<div
  class="flex flex-col relative items-start border-b border-midgrey pb-1 mb-1 overflow-auto flex-1"
>
  {#each groupKeys.slice(page * rowsPerPage + 1, page * rowsPerPage + rowsPerPage) as group, i}
    {#if groupedDuplicates[group] !== undefined}
      <div class="py-1 w-full">
        <DatasetDuplicatesList
          slot="content"
          dataPoints={groupedDuplicates[group]}
          defaultNumberShown={NUMBER_SHOWN}
          groupColumns={groupColumns}
          groupNames={groupNames}
          canvasSpec={canvasSpec}
          selected={selected}
          tooltip={tooltip}
          storybook={storybook}
          candidatesGroupNumber={i}
        />
      </div>
    {/if}
  {/each}
</div>
<PaginationControls
  bind:page
  instancesPerPage={rowsPerPage}
  size={groupKeys.length}
/>
