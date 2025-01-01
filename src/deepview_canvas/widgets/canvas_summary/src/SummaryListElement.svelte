<!-- For licensing see accompanying LICENSE file.
Copyright (C) 2023 betterwithdata Inc. All Rights Reserved. -->

<script lang="ts">
  import type ColumnTable from 'arquero/dist/types/table/column-table';
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
