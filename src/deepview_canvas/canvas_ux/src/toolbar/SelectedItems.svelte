<!-- For licensing see accompanying LICENSE file.
Copyright (C) 2023 betterwithdata Inc. All Rights Reserved. -->

<script lang="ts">
  import type { CanvasSpec, TooltipSpec } from '@betterwithdata/canvas_viz';
  import type ColumnTable from 'arquero/dist/types/table/column-table';
  import type { Readable, Writable } from 'svelte/store';

  import Fa from 'svelte-fa';
  import * as aq from 'arquero';
  import { faCopy } from '@fortawesome/free-solid-svg-icons/faCopy';
  import { faTimes } from '@fortawesome/free-solid-svg-icons/faTimes';

  import { SubHeading, DataSample, IconButton } from '@betterwithdata/canvas_viz';
  import PaginationControls from '@betterwithdata/canvas_viz/dist/ts/elements/PaginationControls.svelte';

  export let table: Readable<ColumnTable>;
  export let selected: Writable<string[]>;
  export let canvasSpec: Writable<CanvasSpec>;
  export let tooltip: Writable<TooltipSpec>;

  let baseCopyText = 'Copy';
  let copyText = baseCopyText;
  let page = 0;
  let elements = [];

  selected.subscribe((sel) => {
    if (sel.length > 0) {
      updateElements(sel);
    } else {
      elements = [];
    }
  });

  async function updateElements(selected: string[]) {
    let selObject = {};
    selObject[$canvasSpec.idColumn] = selected;

    let selTable = aq.table(selObject);
    let filtTable = $table.semijoin(selTable);

    elements = filtTable.objects();
  }

  function clearSelection() {
    selected.set([]);
  }
</script>

<div class="flex flex-col overflow-hidden">
  {#if elements.length > 0}
    <div class="px-2 pt-2 flex items-center justify-between">
      <SubHeading heading={`Selected (${$selected.length})`} />
      <div class="flex">
        <div class="pr-2">
          <IconButton on:click={clearSelection}>
            <Fa icon={faTimes} slot="icon" />
            <span slot="text">Clear</span>
          </IconButton>
        </div>
        <IconButton
          on:mouseleave={() => (copyText = baseCopyText)}
          on:click={() => {
            copyText = 'Copied!';
            navigator.clipboard.writeText(
              JSON.stringify(elements.map((d) => d[$canvasSpec.idColumn]))
            );
          }}
        >
          <Fa icon={faCopy} slot="icon" />
          <span slot="text">{copyText}</span>
        </IconButton>
      </div>
    </div>
    <div class="flex flex-wrap mt-3">
      {#each elements.slice(page * $canvasSpec.instancesPerPage, Math.min(page * $canvasSpec.instancesPerPage + $canvasSpec.instancesPerPage, $selected.length)) as row}
        <DataSample dataPoint={row} {canvasSpec} {selected} {tooltip} />
      {/each}
    </div>
    <PaginationControls
      instancesPerPage={$canvasSpec.instancesPerPage}
      size={$selected.length}
      bind:page
    />
  {/if}
</div>
