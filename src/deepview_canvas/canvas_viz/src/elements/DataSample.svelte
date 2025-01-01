<!-- For licensing see accompanying LICENSE file.
Copyright (C) 2023 betterwithdata Inc. All Rights Reserved. -->

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
