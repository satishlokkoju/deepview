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
    WidgetSpec,
    CanvasSpec,
    TooltipSpec,
  } from '@betterwithdata/canvas_viz';
  import type { Readable, Writable } from 'svelte/store';
  import type { ColumnTable } from 'arquero';

  import createScatterplot from 'regl-scatterplot';
  import { op } from 'arquero';
  import { watchResize } from 'svelte-watch-resize';

  import {
    mapHeightFixed,
    Dropdown,
    getColumnType,
    isStringColumnBinnable,
    ComponentHeader,
  } from '@betterwithdata/canvas_viz';
  import ScatterplotLegend from './ScatterplotLegend.svelte';

  export let canvasSpec: Writable<CanvasSpec>;
  export let tooltip: Writable<TooltipSpec>;
  export let table: Readable<ColumnTable>;
  export let filteredTable: Readable<ColumnTable>;
  export let widgetSpec: WidgetSpec;
  export let fullSize: boolean = false;
  export let selected: Writable<string[]>;

  let container: HTMLDivElement;
  let scatterCanvas: HTMLCanvasElement;
  let idArray: string[];
  let categoryColumn: string;
  let scatterplot: any = undefined;
  let clientX = 0;
  let clientY = 0;
  let selectedLayer: string;
  let target = [0, 0];
  let distance = 1;
  let colorScale = [
    '#308BEF',  // bright blue
    '#4DC960',  // vibrant green
    '#FF9500',  // orange
    '#EF5C53',  // coral red
    '#A34FCD',  // medium purple
    '#00A39B',  // teal
    '#98685E',  // brown
    '#EEDB41',  // yellow
    '#FF6B8B',  // pink
    '#4A90E2',  // sky blue
    '#50E3C2',  // mint
    '#F5A623',  // amber
    '#D0021B',  // deep red
    '#9013FE',  // violet
    '#417505',  // forest green
    '#8B572A',  // chocolate
    '#F8E71C',  // lemon
    '#E056FD',  // magenta
    '#7ED321',  // lime
    '#BD10E0',  // fuchsia
    '#9B9B9B',  // gray
    '#FF7F50',  // coral
    '#4A4A4A',  // charcoal
    '#FFB6C1',  // light pink
    '#20639B'   // navy blue
  ];
  
  $: categories = (() => {
    // Early return if no data or category column
    if (!categoryColumn || !$filteredTable) return [];
    
    const columns = $filteredTable.columnNames();
    
    // Validate category column exists
    if (!columns.includes(categoryColumn)) {
      console.warn(`Category column not found: ${categoryColumn}`);
      categoryColumn = undefined;
      return [];
    }
    
    try {
      return $filteredTable
        .rollup({ col: op.array_agg_distinct(categoryColumn) })
        .object()
        .col ?? [];
    } catch (error) {
      console.error('Error computing categories:', error);
      console.error('Available columns:', $filteredTable.columnNames());
      // Also clear categoryColumn on error
      categoryColumn = undefined;
      return [];
    }
  })();

  $: {
    if (scatterplot !== undefined) {
      const toSelectIds = $selected.map((point: string) =>
        idArray.indexOf(point)
      );
      scatterplot.deselect();
      scatterplot.select(toSelectIds, { preventEvent: true });
    }
  }

  $: categoryColumns = $filteredTable.columnNames().filter((columnName) => {
    return (
      getColumnType($filteredTable, columnName) === 'string' &&
      isStringColumnBinnable(columnName, $filteredTable)
    );
  });

  // Get the column table based on which we look at familiarity
  $: columnNames = $filteredTable.columnNames((d) =>
    d.startsWith('projection_')
  );
  $: layerNames = [
    ...new Set(columnNames.map((name) => name.substring(11, name.length - 2))),
  ];
  $: {
    if (selectedLayer === undefined)
      selectedLayer = layerNames[0] === undefined ? '' : layerNames[0];
  }
  $: xColumn =
    selectedLayer === undefined
      ? undefined
      : columnNames.find(
          (name) => name.includes(selectedLayer) && name.endsWith('_x')
        )!;
  $: yColumn =
    selectedLayer === undefined
      ? undefined
      : columnNames.find(
          (name) => name.includes(selectedLayer) && name.endsWith('_y')
        )!;

  $: if (scatterCanvas !== undefined) {
    if (scatterplot !== undefined) {
      scatterplot.destroy();
    }
    scatterplot = createScatterplot({
      canvas: scatterCanvas,
      lassoInitiator: true,
      colorBy: 'valueA',
      deselectOnDblClick: false,
      deselectOnEscape: false,
      pointColor: colorScale,
    });
    scatterplot.subscribe('select', selectPoints);
    scatterplot.subscribe('pointOver', hoverPoint);
    scatterplot.subscribe('pointOut', () =>
      tooltip.update((t: TooltipSpec) => {
        t.hover = false;
        return { ...t };
      })
    );
  }

  $: if (
    xColumn !== undefined &&
    yColumn !== undefined &&
    scatterplot !== undefined
  ) {
    const points: number[][] = [];
    const table = $filteredTable;
    const xArray = table.array(xColumn);
    const yArray = table.array(yColumn);
    let maxX = 0,
      minX = 0,
      maxY = 0,
      minY = 0;
    idArray = table.array($canvasSpec.idColumn) as string[];

    if (categoryColumn !== undefined) {
      const categoryArray = table.array(categoryColumn);
      const categories = table
        .groupby(categoryColumn)
        .count()
        .array(categoryColumn) as string[];
      xArray.forEach((item, i) => {
        maxX = maxX > item ? maxX : item;
        minX = minX < item ? minX : item;
        maxY = maxY > item ? maxY : item;
        minY = minY < item ? minY : item;
        points.push([item, yArray[i], categories.indexOf(categoryArray[i])]);
      });
    } else {
      xArray.forEach((item, i) => points.push([item, yArray[i]]));
    }
    distance = Math.max(maxX - minX, maxY - minY) / 2;
    target = [(maxX + minX) / 2, (maxY + minY) / 2];
    initPoints(points);
  }

  function initPoints(points: number[][]) {
    scatterplot.set({
      cameraTarget: target,
      cameraDistance: distance,
      pointSize: 15,
    });
    scatterplot.clear();
    const drawPromise = scatterplot.draw(points);
    drawPromise.then(initialSelect);
  }

  function initialSelect() {
    const toSelectIds = $selected.map((point: string) =>
      idArray.indexOf(point)
    );
    scatterplot.select(toSelectIds, { preventEvent: true }); // TODO: Why does this not work?
  }

  function selectPoints(points: any) {
    let toSelectIds = points.points.map((d) => idArray[d]);
    let currentlySelected: Set<string> = new Set<string>($selected);

    toSelectIds.forEach((id: string) => {
      if (currentlySelected.has(id)) {
        currentlySelected.delete(id);
      } else {
        currentlySelected.add(id);
      }
    });
    selected.set(Array.from(currentlySelected));
  }

  function hoverPoint(point: any) {
    let row: Record<string, unknown> = {};
    $table.columnNames().forEach((col) => {
      row[col] = $filteredTable.get(col, point);
    });
    tooltip.set({
      hover: true,
      mousePos: { x: clientX, y: clientY },
      fetchPrefix: $canvasSpec.filesPath,
      instance: row,
    });
  }

  function handleKeydown(event: MouseEvent) {
    scatterplot.set({
      cameraTarget: target,
      cameraDistance: distance,
    });
  }

  function resized() {
    if (scatterplot !== undefined) {
      scatterplot.destroy();
    }
    scatterplot = createScatterplot({
      canvas: scatterCanvas,
      lassoInitiator: true,
      colorBy: 'valueA',
      deselectOnDblClick: false,
      deselectOnEscape: false,
      pointColor: colorScale,
    });
    scatterplot.subscribe('select', selectPoints);
    scatterplot.subscribe('pointOver', hoverPoint);
    scatterplot.subscribe('pointOut', () =>
      tooltip.update((t: TooltipSpec) => {
        t.hover = false;
        return { ...t };
      })
    );
  }
</script>

<svelte:window
  on:mousemove={(ev) => {
    clientX = ev.clientX;
    clientY = ev.clientY;
  }}
/>

<div
  class="flex flex-col p-2 {fullSize
    ? 'h-full'
    : mapHeightFixed(widgetSpec.height)}"
>
  <ComponentHeader
    title={'Scatterplot'}
    description={widgetSpec.description}
    {container}
  >
    {#if layerNames.length > 1}
      <div class="mr-4 flex flex-row mb-2 items-center">
        <p class="mr-2">Layer:</p>
        <Dropdown items={layerNames} bind:value={selectedLayer} />
      </div>
    {/if}
    {#if categoryColumns.length > 0}
      <div class="mr-4 flex flex-row mb-2 items-center">
        <p class="mr-2">Category column:</p>
        <Dropdown bind:value={categoryColumn} items={categoryColumns} />
      </div>
    {/if}
  </ComponentHeader>
  <div>Double-click to recenter. Shift-click and drag to lasso-select.</div>
  <div
    bind:this={container}
    class="flex-grow relative"
    on:dblclick={handleKeydown}
    use:watchResize={resized}
    role="application"
    aria-label="Interactive scatterplot visualization"
  >
    {#if xColumn !== undefined && yColumn !== undefined}
      <canvas bind:this={scatterCanvas} />
      <ScatterplotLegend {categories} {colorScale} />
    {:else}
      <p>
        There needs to be both a column starting with 'projection_' and ending
        on '_x' and one starting with 'projection_' and ending on '_y'.
      </p>
    {/if}
  </div>
</div>
