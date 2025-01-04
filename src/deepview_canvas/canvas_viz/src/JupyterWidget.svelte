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
  import type { DOMWidgetModel } from "@jupyter-widgets/base";
  import type { SvelteComponent } from "svelte";
  import type { WidgetSpec, SummaryWidgetSpec } from "./types";

  import {
    selected,
    filter,
    groupColumns,
    groupNames,
    canvasSpec,
    dataTable,
    filterError,
    tooltip,
    table,
    filteredTable,
    groupedTables,
    widgetWritable,
    initializeStores,
  } from "./stores";

  import { DataSampleDetail } from "./elements";

  export let model: DOMWidgetModel;
  export let widget: SvelteComponent;

  initializeStores(model);

  let widgetSpec = widgetWritable<WidgetSpec | SummaryWidgetSpec>(
    "widget_spec",
    model.attributes.widget_spec
  );
  widgetSpec.setModel(model);

  function handleSpecChanged(event: CustomEvent) {
    widgetSpec.set(event.detail.spec);
  }
</script>

{#if $table && $widgetSpec}
  <div
    class="{$widgetSpec.name === 'toolbar'
      ? 'border-midgrey border-2'
      : ''} mt-2 h-full"
    style="min-height: 350px"
  >
    <svelte:component
      this={widget}
      widgetSpec={$widgetSpec}
      on:specChanged={handleSpecChanged}
      {selected}
      {filter}
      {groupColumns}
      {groupNames}
      {canvasSpec}
      {dataTable}
      {filterError}
      {tooltip}
      {table}
      {filteredTable}
      {groupedTables}
      notebook={true}
    />
  </div>
{:else}
  No data to show.
{/if}
<DataSampleDetail {tooltip} {canvasSpec} />
