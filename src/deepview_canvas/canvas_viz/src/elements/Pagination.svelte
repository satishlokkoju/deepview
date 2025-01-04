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
  import type ColumnTable from "arquero/dist/types/table/column-table";
  import type { Writable } from "svelte/store";
  import type { CanvasSpec, TooltipSpec } from "../types";

  import { selectAll } from "../helpers/selection";
  import IconButton from "./IconButton.svelte";
  import DataSample from "./DataSample.svelte";
  import PaginationControls from "./PaginationControls.svelte";

  import Fa from "svelte-fa";
  import { faCheckSquare } from "@fortawesome/free-solid-svg-icons/faCheckSquare";

  export let title: string;
  export let filteredTable: ColumnTable;
  export let selected: Writable<string[]>;
  export let canvasSpec: Writable<CanvasSpec>;
  export let tooltip: Writable<TooltipSpec>;
  export let storybook: boolean = false;

  let page = 0;
  function resetPage() {
    page = 0;
  }

  $: {
    filteredTable;
    resetPage();
  }

  $: dataPoints = filteredTable
    .slice(
      page * $canvasSpec.instancesPerPage,
      Math.min(
        page * $canvasSpec.instancesPerPage + $canvasSpec.instancesPerPage,
        filteredTable.size
      )
    )
    .objects();
</script>

<div class="w-full border rounded-md border-midgrey p-2">
  <div
    class="flex items-center mb-2 justify-between border-b pb-1 border-midgrey"
  >
    <h3 class="font-bold whitespace-nowrap mr-3">
      {title}
    </h3>
    <IconButton
      uiChange={true}
      on:click={() => {
        selectAll(
          selected,
          dataPoints.map((d) => d[$canvasSpec.idColumn])
        );
      }}
    >
      <Fa icon={faCheckSquare} slot="icon" />
    </IconButton>
  </div>
  <div
    class="flex flex-nowrap items-top border-b border-midgrey justify-between"
  >
    <div class="flex flex-wrap content-top">
      {#each dataPoints as dataPoint}
        <DataSample
        {dataPoint}
        {canvasSpec}
        {selected}
        {tooltip}
        {storybook} />
      {/each}
    </div>
    <slot name="extra" />
  </div>
  <PaginationControls
    bind:page
    size={filteredTable.size}
    instancesPerPage={$canvasSpec.instancesPerPage}
  />
</div>
