<!-- For licensing see accompanying LICENSE file.
Copyright (C) 2023 betterwithdata Inc. All Rights Reserved. -->

<script lang="ts">
  import type { CanvasSpec, TooltipSpec } from "../types";
  import type { Writable } from "svelte/store";

  import Fa from "svelte-fa";
  import { fade } from "svelte/transition";
  import { faChartBar } from "@fortawesome/free-solid-svg-icons/faChartBar";

  import { getComponentForType } from "../helpers/filetype";

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
            <span class="text-bold">{key}:</span>
            <span class="ml-2 ">
              {Array.isArray(val)
                ? val
                : isNaN(Number.parseFloat(val))
                ? val
                : Number.parseFloat(val).toFixed(2)}
            </span>
          </div>
        {/if}
      {/each}
    </div>
  </div>
{/if}
