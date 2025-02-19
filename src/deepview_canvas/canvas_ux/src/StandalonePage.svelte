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
    Widget,
    CanvasSpec,
    TooltipSpec,
    WidgetSpec,
    SummaryWidgetSpec,
  } from '@betterwithdata/canvas_viz';
  import type { Readable, Writable } from 'svelte/store';
  import type { SvelteComponent } from 'svelte';
  import type { ColumnTable } from 'arquero';

  import { mapHeight, mapWidth } from '@betterwithdata/canvas_viz';

  import StandaloneWidget from './StandaloneWidget.svelte';

  export let filter: Writable<string>;
  export let filterError: Writable<string>;
  export let table: Readable<ColumnTable>;
  export let canvasSpec: Writable<CanvasSpec>;
  export let groupColumns: Writable<string[]>;
  export let groupNames: Writable<string[][]>;
  export let groupedTables: Readable<ColumnTable[]>;
  export let filteredTable: Readable<ColumnTable>;
  export let selected: Writable<string[]>;
  export let tooltip: Writable<TooltipSpec>;
  export let widgets: Widget[];
  export let components: Record<string, typeof SvelteComponent>;
  export let widgetSpecs: Writable<
    Record<string, WidgetSpec | SummaryWidgetSpec>
  >;
  export let storybook: boolean = true;

  $: fullSize = widgets.length === 1;
</script>

<div class={fullSize ? 'h-full w-full' : 'grid grid-cols-6 main-grid gap-2'}>
  {#each widgets as widget}
    <div
      class={fullSize
        ? 'h-full w-full'
        : `${mapHeight(widget.height)} ${mapWidth(
            widget.width
          )} border-2 border-midgrey rounded`}
    >
      <StandaloneWidget
        {widget}
        fullSize={false}
        {filter}
        {filterError}
        {table}
        {canvasSpec}
        {groupColumns}
        {groupNames}
        {groupedTables}
        {filteredTable}
        {selected}
        {tooltip}
        {components}
        {storybook}
        {widgetSpecs}
      />
    </div>
  {/each}
</div>
