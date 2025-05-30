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
  import type { DataMapSpec, CanvasSpec } from '@betterwithdata/canvas_viz';
  import type { Writable, Readable } from 'svelte/store';
  import type { ColumnTable } from 'arquero';
  import type { VegaLiteSpec } from 'svelte-vega';

  import { VegaLite } from 'svelte-vega';

  import { mapHeightFixed, ComponentHeader } from '@betterwithdata/canvas_viz';

  export let table: Readable<ColumnTable>;
  export let filteredTable: Readable<ColumnTable>;
  export let widgetSpec: DataMapSpec;
  export let fullSize: boolean = false;
  export let canvasSpec: Writable<CanvasSpec>;

  let container: HTMLDivElement;

  let vegaSchema: VegaLiteSpec | undefined = undefined;
  let unmapped: Record<string, number> = {};

  $: if (container !== undefined) {
    let mapped = false;
    const width =
      container.offsetWidth > 100
        ? container.offsetWidth - 100
        : container.offsetWidth;
    const height =
      container.offsetHeight > 200
        ? container.offsetHeight - 30
        : container.offsetHeight;
    const groups = $filteredTable.groupby(widgetSpec.idColumn);
    const groupsRaw = $table.groupby(widgetSpec.idColumn);
    let data: Record<number, { id: number; count: number; name: string }> = {};
    let maxCount = 0;
    let partitions = groups.partitions();
    let partitionsRaw = groupsRaw.partitions();
    partitions.forEach((partition: number[]) => {
      const subTable = $filteredTable.reify(partition);
      const id = subTable.get(widgetSpec.idColumn);
      if (typeof id === 'number') {
        const name = Object.keys(widgetSpec.idMap).find(
          (key) => widgetSpec.idMap[key] === id
        );
        if (name !== undefined) {
          data[id] = {
            id: id,
            count: subTable.size,
            name: name,
          };
        } else {
          unmapped[id] = subTable.size;
        }
      } else {
        if (widgetSpec.idMap[id] !== undefined) {
          mapped = true;
          data[widgetSpec.idMap[id]] = {
            id: widgetSpec.idMap[id],
            count: subTable.size,
            name: id,
          };
        } else {
          unmapped[id] = subTable.size;
        }
      }
    });
    if ($canvasSpec.showUnfilteredData) {
      partitionsRaw.forEach((partition: number[]) => {
        const subTable = $filteredTable.reify(partition);
        const count = subTable.size;
        maxCount = maxCount > count ? maxCount : count;
      });
    } else {
      Object.values(data).forEach(
        (value) => (maxCount = maxCount > value.count ? maxCount : value.count)
      );
    }
    for (const [key, value] of Object.entries(widgetSpec.idMap)) {
      if (data[value] === undefined) {
        data[value] = { id: value, count: 0, name: key };
      }
    }
    const fields = mapped ? ['name', 'count'] : ['count'];
    const tooltip = mapped
      ? [
          { field: 'name', type: 'nominal', title: 'Name' },
          { field: 'count', type: 'quantitative', title: 'Value' },
        ]
      : [{ field: 'count', type: 'quantitative', title: 'Value' }];
    vegaSchema = {
      $schema: 'https://vega.github.io/schema/vega-lite/v5.json',
      width: width,
      height: height,
      data: {
        url: widgetSpec.mapUrl,
        format: {
          type: 'topojson',
          feature: widgetSpec.feature,
        },
      },
      transform: [
        {
          lookup: 'id',
          from: {
            data: { values: Object.values(data) },
            key: 'id',
            fields: fields,
          },
        },
      ],
      projection: {
        type: widgetSpec.projection,
      },
      mark: { type: 'geoshape', stroke: 'black' },
      encoding: {
        color: {
          field: 'count',
          type: 'quantitative',
          scale: { domain: [0, maxCount] },
        },
        tooltip: tooltip,
      },
    };
  }
</script>

<div
  class="flex flex-col {fullSize
    ? 'h-full'
    : mapHeightFixed(widgetSpec.height)}"
>
  <ComponentHeader
    title={'Data Map'}
    description={widgetSpec.description}
    {container}
  >
    {#each Object.keys(unmapped) as unmappedElement}
      <p class="px-2 pb-2 pt-2">
        {unmappedElement}: {unmapped[unmappedElement]}
      </p>
    {/each}
  </ComponentHeader>
  <div bind:this={container} class="overflow-auto flex-grow">
    {#if vegaSchema !== undefined}
      <VegaLite spec={vegaSchema} options={{ actions: false }} />
    {/if}
  </div>
</div>
