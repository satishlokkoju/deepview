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
  import type { Readable, Writable } from 'svelte/store';
  import type { CanvasSpec, TooltipSpec } from '@betterwithdata/canvas_viz';

  import FilterBar from './FilterBar.svelte';
  import SelectedItems from './SelectedItems.svelte';
  import Settings from './Settings.svelte';
  import Grouping from './Grouping.svelte';

  export let notebook: boolean = false;
  export let filter: Writable<string>;
  export let filterError: Writable<string>;
  export let table: Readable<ColumnTable>;
  export let canvasSpec: Writable<CanvasSpec>;
  export let groupColumns: Writable<string[]>;
  export let groupNames: Writable<string[][]>;
  export let groupedTables: Readable<ColumnTable[]>;
  export let selected: Writable<string[]>;
  export let tooltip: Writable<TooltipSpec>;
</script>

<div
  class="flex flex-col h-full bg-lightgrey "
  style="width: {notebook ? '35rem' : '25rem'}; 
        max-width: {notebook ? '35rem' : '25rem'};
        "
>
  <div class="p-2 overflow-y-auto h-full">
    <Settings {canvasSpec} />
    <FilterBar {filter} {filterError} {table} />
    <Grouping {table} {groupColumns} {groupNames} {groupedTables} {filter} />
    <SelectedItems {table} {canvasSpec} {selected} {tooltip} />
  </div>
</div>

<style global>
  @tailwind base;
  @tailwind components;
  @tailwind utilities;
</style>
