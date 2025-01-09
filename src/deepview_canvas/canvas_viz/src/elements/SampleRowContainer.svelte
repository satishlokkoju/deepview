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

  import DataSample from "./DataSample.svelte";
  import IconButton from "./IconButton.svelte";

  import Fa from "svelte-fa";
  import { faEyeSlash } from "@fortawesome/free-solid-svg-icons/faEyeSlash";
  import { faEye } from "@fortawesome/free-solid-svg-icons/faEye";

  export let defaultNumberShown: number = 20;
  export let dataPoints: Record<string, unknown>[];
  export let selected: Writable<string[]>;
  export let canvasSpec: Writable<CanvasSpec>;
  export let tooltip: Writable<TooltipSpec>;
  export let storybook: boolean = false;
  let numberShown = defaultNumberShown;
</script>

<div class="flex flex-wrap items-center justify-between flex-1">
  <div class="flex flex-wrap">
    {#each dataPoints.slice(0, numberShown) as dataPoint}
      <DataSample {dataPoint} {canvasSpec} {selected} {tooltip} {storybook} />
    {/each}
  </div>
  {#if dataPoints.length > numberShown}
    <IconButton on:click={() => (numberShown = dataPoints.length)}>
      <Fa icon={faEye} slot="icon" />
      <p slot="text">Show {dataPoints.length - defaultNumberShown} more</p>
    </IconButton>
  {/if}
  {#if dataPoints.length === numberShown && dataPoints.length > defaultNumberShown}
    <IconButton on:click={() => (numberShown = defaultNumberShown)}>
      <Fa icon={faEyeSlash} slot="icon" />
      <p slot="text">Collapse</p>
    </IconButton>
  {/if}
</div>
