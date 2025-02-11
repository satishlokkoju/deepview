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
  import { ResolverType, CanvasSpec, TooltipSpec } from '@betterwithdata/canvas_viz';
  import type { ColumnTable } from 'arquero';
  import type { Writable } from 'svelte/store';

  import { CanvasVegaLite, Pagination } from '@betterwithdata/canvas_viz';
  import { desc } from 'arquero';

  export let table: ColumnTable;
  export let filteredTable: ColumnTable;
  export let groupedTables: ColumnTable[];
  export let groupNames: Writable<string[][]>;
  export let canvasSpec: Writable<CanvasSpec>;
  export let selected: Writable<string[]>;
  export let tooltip: Writable<TooltipSpec>;
  export let selectedColumn: string;
  export let sortDescending: boolean;
  export let storybook: boolean = false;

  let container: HTMLDivElement;

  $: sortTables(sortDescending, $groupNames, filteredTable, groupedTables);
  $: histogramSpec = {
    $schema: 'https://vega.github.io/schema/vega-lite/v5.json',
    title: `${selectedColumn} binned`,
    data: { values: 'values' },
    mark: { type: 'bar', tooltip: true },
    encoding: {
      x: {
        field: 'bin_0',
        title: 'score',
      },
      y: { field: 'count', type: 'quantitative', title: 'instances' },
    },
  };
  $: filteredStatistics = filteredTable.rollup({
    mean: `d => op.mean(d.${selectedColumn})`,
    std: `d => op.stdev(d.${selectedColumn})`,
  });
  $: groupedStatistics = groupedTables.map((table) => {
    return table.rollup({
      mean: `d => op.mean(d.${selectedColumn})`,
      std: `d => op.stdev(d.${selectedColumn})`,
    });
  });

  function sortTables(
    sortDescending: boolean,
    groupNames: string[][],
    table: ColumnTable,
    tables: ColumnTable[]
  ) {
    if (groupNames.length === 0) {
      filteredTable = table.orderby(
        sortDescending ? desc(selectedColumn) : selectedColumn
      );
    } else {
      groupedTables = [
        ...tables.map((table) =>
          table.orderby(sortDescending ? desc(selectedColumn) : selectedColumn)
        ),
      ];
    }
  }
</script>

<div class="flex justify-between overflow-hidden flex-grow">
  <div class="flex flex-col overflow-hidden flex-1">
    <div class="flex overflow-hidden" bind:this={container}>
      {#if $groupNames.length === 0}
        <Pagination
          title="{sortDescending ? 'Most' : 'Least'} Familiar Instances"
          {filteredTable}
          {selected}
          {tooltip}
          {canvasSpec}
          {storybook}
        >
          <div class="flex flex-col items-center" slot="extra">
            <CanvasVegaLite
              showUnfilteredData={$canvasSpec.showUnfilteredData}
              spec={histogramSpec}
              data={{ values: 'arrow_table' }}
              resolver={{
                columnName: selectedColumn,
                type: ResolverType.NUMBER,
              }}
              {table}
              {filteredTable}
            />
      
            <p class="text-xs text-darkgrey">
              {#if filteredStatistics.get('mean', 0) !== undefined}
              Mean: {filteredStatistics.get('mean', 0).toFixed(2)}
              {/if}
              {#if filteredStatistics.get('std', 0) !== undefined}
              Std: {filteredStatistics.get('std', 0).toFixed(2)}
              {/if}
            </p>
          </div>
        </Pagination>
      {:else}
        <div class="flex flex-wrap overflow-auto w-full">
          {#each groupedTables as groupTable, i}
            {#if groupTable.size !== 0}
              <div class="flex flex-col pb-2 overflow-hidden flex-grow">
                <Pagination
                  title={$groupNames[i].join(' | ')}
                  filteredTable={groupTable}
                  {selected}
                  {tooltip}
                  {canvasSpec}
                  {storybook}
                >
                  <div class="flex flex-col items-center" slot="extra">
                    <CanvasVegaLite
                      showUnfilteredData={$canvasSpec.showUnfilteredData}
                      spec={histogramSpec}
                      data={{ values: 'arrow_table' }}
                      resolver={{
                        columnName: selectedColumn,
                        type: ResolverType.NUMBER,
                      }}
                      {table}
                      filteredTable={groupTable}
                    />
                    <p class="text-xs text-darkgrey">
                      {#if groupedStatistics[i].get('mean', 0) !== undefined}
                      Mean: {groupedStatistics[i].get('mean', 0).toFixed(2)}
                      {/if}
                      {#if groupedStatistics[i].get('std', 0) !== undefined}
                      Std: {groupedStatistics[i].get('std', 0).toFixed(2)}
                      {/if}
                    </p>
                  </div>
                </Pagination>
              </div>
            {/if}
          {/each}
        </div>
      {/if}
    </div>
  </div>
</div>
