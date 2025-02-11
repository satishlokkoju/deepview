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
    SummaryWidgetSpec,
    WidgetSpec,
    CanvasSpec,
    TooltipSpec,
  } from '@betterwithdata/canvas_viz';
  import type { Readable, Writable } from 'svelte/store';
  import type { ColumnTable } from 'arquero';

  import { onDestroy, SvelteComponent } from 'svelte';
  import { mapHeight, mapWidth } from '@betterwithdata/canvas_viz';

  export let widget: Widget;
  export let fullSize: boolean;
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
  export let components: Record<string, typeof SvelteComponent>;
  export let storybook: boolean = true;
  export let widgetSpecs: Writable<
    Record<string, WidgetSpec | SummaryWidgetSpec>
  >;

  let widgetSpec: WidgetSpec | SummaryWidgetSpec;
  let oldWidgetType: string;
  let target: HTMLDivElement;
  let cmp: SvelteComponent | undefined;

  $: {
    if ($widgetSpecs[widget.name] !== undefined) {
      widgetSpec = $widgetSpecs[widget.name];
      oldWidgetType = widget.name;
    } else {
      // Need to reload if the widget changes while this view is reused.
      loadSpec(widget);
    }
  }

  $: component = components[widget.name];

  $: if (target && component && oldWidgetType == widget.name) {
    cleanup();
    create();
  }

  $: if (cmp) {
    cmp.$set({
      widgetSpec: widgetSpec,
      fullSize: fullSize,
      filter: filter,
      filterError: filterError,
      table: table,
      vertical: true,
      canvasSpec: canvasSpec,
      groupColumns: groupColumns,
      groupNames: groupNames,
      groupedTables: groupedTables,
      filteredTable: filteredTable,
      selected: selected,
      tooltip: tooltip,
      storybook: storybook,
    });
  }

  async function loadSpec(widget: Widget) {
    const infoQuery = await fetch(`data/${widget.name}.json`);
    const preparsedData = (await infoQuery.json()) as
      | WidgetSpec
      | SummaryWidgetSpec;
    widgetSpec = preparsedData;
    oldWidgetType = widget.name;
  }

  function handleSpecChanged(event: CustomEvent) {
    widgetSpec = event.detail.spec;
    let changedSpec = $widgetSpecs;
    changedSpec[widget.name] = event.detail.spec;
    widgetSpecs.set({ ...changedSpec });
  }

  function cleanup() {
    if (cmp === undefined) return;
    cmp.$destroy();
    cmp = undefined;
  }

  function create() {
    cmp = new component({
      target,
      props: {
        widgetSpec: widgetSpec,
        fullSize: fullSize,
        filter: filter,
        filterError: filterError,
        table: table,
        vertical: true,
        canvasSpec: canvasSpec,
        groupColumns: groupColumns,
        groupNames: groupNames,
        groupedTables: groupedTables,
        filteredTable: filteredTable,
        selected: selected,
        tooltip: tooltip,
        storybook: storybook,
      },
    });
    cmp.$on('specChanged', handleSpecChanged);
  }

  onDestroy(cleanup);
</script>

<div
  class={fullSize
    ? 'h-full w-full'
    : `${mapHeight(widget.height)} ${mapWidth(widget.width)}`}
  bind:this={target}
/>
