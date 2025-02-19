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
    SummaryElement,
    SummaryWidgetSpec,
    CanvasSpec,
  } from '@betterwithdata/canvas_viz';
  import type { ColumnTable } from 'arquero';
  import type { Writable } from 'svelte/store';

  import Fa from 'svelte-fa';
  import { createEventDispatcher } from 'svelte';
  import { faEdit } from '@fortawesome/free-solid-svg-icons/faEdit';
  import { faCheck } from '@fortawesome/free-solid-svg-icons/faCheck';
  import { faTimes } from '@fortawesome/free-solid-svg-icons/faTimes';

  import { mapHeight, IconButton, ComponentHeader } from '@betterwithdata/canvas_viz';

  import { extractColumnElements } from './summarySpecs';
  import SummaryListElement from './SummaryListElement.svelte';
  import SummaryNumberElement from './SummaryNumberElement.svelte';
  import SummaryChartSelection from './SummaryChartSelection.svelte';

  export let canvasSpec: Writable<CanvasSpec>;
  export let table: Writable<ColumnTable>;
  export let filteredTable: Writable<ColumnTable>;
  export let widgetSpec: SummaryWidgetSpec;
  export let fullSize: boolean = false;

  const dispatch = createEventDispatcher();
  let editMode = false;
  let userSpecUpdate = false;
  let container: HTMLDivElement;

  $: elements =
    widgetSpec.summaryElements.length === 0 && !userSpecUpdate
      ? extractColumnElements($table)
      : widgetSpec.summaryElements;
  $: numberData = elements.filter((row) => typeof row.data === 'number');
  $: chartData = elements.filter((row) => typeof row.data !== 'number');

  function updateSpecElements(newElements: SummaryElement[]) {
    const newSpec = { ...widgetSpec, summaryElements: newElements };
    dispatch('specChanged', { spec: newSpec });
  }

  function removeElement(element: SummaryElement) {
    userSpecUpdate = true;
    let newElements = elements.filter(
      (el) => el.name !== element.name || el.data !== element.data
    );
    updateSpecElements(newElements);
  }

  function addElement(event: CustomEvent) {
    userSpecUpdate = true;
    let newElements = [...elements, event.detail.element];
    updateSpecElements(newElements);
  }

  function updateElement(element: SummaryElement, oldElement: SummaryElement) {
    userSpecUpdate = true;
    let elementIndex = elements.findIndex(
      (el) => el.name === oldElement.name && el.data === oldElement.data
    );
    const newElements = elements.slice();
    newElements[elementIndex] = element;
    updateSpecElements(newElements);
  }
</script>

<div
  class="flex flex-col p-2 {fullSize ? 'h-full' : mapHeight(widgetSpec.height)}"
>
  <ComponentHeader
    title={'Summary'}
    description={widgetSpec.description}
    {container}
  >
    <div>
      <IconButton on:click={() => (editMode = !editMode)}>
        <Fa icon={editMode ? faCheck : faEdit} slot="icon" />
        <span slot="text">{editMode ? 'Done' : 'Edit'}</span>
      </IconButton>
    </div>
  </ComponentHeader>
  {#if editMode}
    <SummaryChartSelection table={$table} on:elementSelected={addElement} />
  {/if}
  <div class="flex flex-col overflow-auto" bind:this={container}>
    {#if CharacterData.length > 0 || numberData.length > 0}
      <div class="flex flex-wrap">
        {#each numberData as element}
          <div class="relative">
            <SummaryNumberElement
              data={element.data}
              name={element.name}
              {editMode}
            />
            {#if editMode}
              <button
                class="absolute top-0 right-0"
                on:click={() => removeElement(element)}
              >
                <Fa icon={faTimes} />
              </button>
            {/if}
          </div>
        {/each}
      </div>
      <div class="flex flex-wrap">
        {#each chartData as element}
          <div class="relative">
            <SummaryListElement
              table={$table}
              filteredTable={$filteredTable}
              canvasSpec={$canvasSpec}
              {element}
              {editMode}
              on:update={(event) =>
                updateElement(event.detail.element, event.detail.oldElement)}
            />
            {#if editMode}
              <button
                class="absolute top-0 right-0"
                on:click={() => removeElement(element)}
              >
                <Fa icon={faTimes} />
              </button>
            {/if}
          </div>
        {/each}
      </div>
    {:else}
      <p>There was no data found to display in the summary charts.</p>
    {/if}
  </div>
</div>
