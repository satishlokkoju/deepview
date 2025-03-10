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
  import type { CanvasSpec, TooltipSpec } from '@betterwithdata/canvas_viz';
  import type { ColumnTable } from 'arquero';
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
              JSON.stringify(elements.map((d) => {
                // Use filename if it exists, otherwise use the configured ID column
                return d.filename !== undefined ? d.filename : d[$canvasSpec.idColumn];
              }))
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
