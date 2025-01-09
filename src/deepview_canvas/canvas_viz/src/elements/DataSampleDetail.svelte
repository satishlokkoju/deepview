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

  import Fa from "svelte-fa";
  import { fade } from "svelte/transition";
  import { faChartBar } from "@fortawesome/free-solid-svg-icons/faChartBar";

  import { getComponentForType } from "../helpers/filetype";

  const formatValue = (val: any): string => {
    if (Array.isArray(val)) 
      return val.toString();
    if (typeof val === 'number') 
      return val.toFixed(2);
    return val;
  };

  export let canvasSpec: Writable<CanvasSpec>;
  export let tooltip: Writable<TooltipSpec>;
  export let storybook: boolean = false;

  let windowWidth = 0;
  let windowHeight = 0;
  let tooltipWidth = 0;
  let tooltipHeight = 0;
  $: yPos =
    windowHeight > $tooltip.mousePos.y + tooltipHeight
      ? $tooltip.mousePos.y
      : $tooltip.mousePos.y - tooltipHeight - 20;
  $: xStyle =
    windowWidth > $tooltip.mousePos.x + tooltipWidth + 10
      ? `left: ${$tooltip.mousePos.x}px;`
      : `right: 10px;`;
  $: style = `top: ${yPos}px; ${xStyle}; background: black`;
</script>

<svelte:window bind:innerWidth={windowWidth} bind:innerHeight={windowHeight} />
{#if $tooltip.hover && $tooltip.instance !== undefined}
  <div
    class="text-sm fixed p-1 rounded text-text-dark shadow z-10 flex mt-4 mb-4"
    {style}
    transition:fade
    bind:offsetWidth={tooltipWidth}
    bind:offsetHeight={tooltipHeight}
  >
    <div class="flex flex-shrink-0">
      <svelte:component
        this={getComponentForType($canvasSpec.dataType)}
        id={$tooltip.instance[$canvasSpec.idColumn]}
        {canvasSpec}
        {storybook}
        large={true}
      />
    </div>
    <div class="flex flex-col pl-2 pr-4 m-2 mt-0 break-all">
      <div class="flex font-bold">
        {$tooltip.instance[$canvasSpec.idColumn]}
      </div>
      {#if $tooltip.number !== undefined}
        <div class="flex flex-nowrap">
          <Fa icon={faChartBar} />
          <span class="ml-2">{$tooltip.number}</span>
        </div>
      {/if}
      {#each Object.entries($tooltip.instance) as [key, val]}
        {#if key !== $canvasSpec.idColumn && !key.startsWith("familiarity_") && !key.startsWith("duplicates_") && !key.startsWith("projection_") && !key.startsWith("splitFamiliarity")}
          <div class="flex flex-nowrap">
            <span class="font-bold">{key}:</span>
            <span class="ml-2">
              {formatValue(val)}
            </span>
          </div>
        {/if}
      {/each}
    </div>
  </div>
{/if}
