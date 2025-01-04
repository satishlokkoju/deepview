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
  import type { CanvasSpec, TooltipSpec } from "../types";
  import type { Writable } from "svelte/store";
  import Icon from "svelte-fa";
  import { faCheckSquare } from "@fortawesome/free-solid-svg-icons/faCheckSquare";

  import { getComponentForType } from "../helpers/filetype";

  export let dataPoint: Record<string, unknown>;
  export let canvasSpec: Writable<CanvasSpec>;
  export let selected: Writable<string[]>;
  export let tooltip: Writable<TooltipSpec>;
  export let number: number | undefined = undefined;
  export let storybook: boolean = false;

  $: id = dataPoint[$canvasSpec.idColumn] as string;

  let hover = false;
  let m = { x: 0, y: 0 };

  function select() {
    const index = $selected.indexOf(id);
    if (index > -1) {
      selected.update((d: string[]) => {
        d.splice(index, 1);
        return [...d];
      });
    } else {
      selected.set([...$selected, id]);
    }
  }

  function handleMousemove(event: MouseEvent) {
    m.x = event.clientX;
    m.y = event.clientY;
    updateSampleTooltip();
  }

  function updateSampleTooltip() {
    tooltip.set({
      hover: hover,
      mousePos: m,
      fetchPrefix: $canvasSpec.filesPath,
      instance: dataPoint,
      number: number,
    });
  }
</script>

<div
  on:mouseenter={() => {
    hover = true;
    updateSampleTooltip();
  }}
  on:mouseleave={() => {
    hover = false;
    updateSampleTooltip();
  }}
  on:mousemove={handleMousemove}
  class="relative"
>
  <svelte:component
    this={getComponentForType($canvasSpec.dataType)}
    {id}
    {canvasSpec}
    {storybook}
    on:click={() => select()}
  />
  {#if $selected.includes(id)}
    <Icon
      class="absolute top-0 right-0 bg-white border-2 border-white"
      icon={faCheckSquare}
    />
  {/if}
</div>
