<!-- # Copyright 2024 BetterWithData
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
  import type { CanvasSpec, TooltipSpec } from '@betterwithdata/canvas_viz';
  import type { Writable } from 'svelte/store';

  import {
    SampleRowContainer,
    Container,
    selectAll,
    IconButton,
  } from '@betterwithdata/canvas_viz';

  import Fa from 'svelte-fa';
  import { faCheckSquare } from '@fortawesome/free-solid-svg-icons/faCheckSquare';

  export let dataPoints: Record<string, unknown>[];
  export let groupColumns: Writable<string[]>;
  export let groupNames: Writable<string[][]>;
  export let selected: Writable<string[]>;
  export let canvasSpec: Writable<CanvasSpec>;
  export let tooltip: Writable<TooltipSpec>;
  export let defaultNumberShown: number;
  export let storybook = false;
  export let candidatesGroupNumber: number;

  $: filteredPoints = $groupNames
    .map((attrs: string[]) => {
      return {
        attrs: attrs,
        points: dataPoints.filter((point: Record<string, unknown>) => {
          let match = true;
          attrs.forEach((attr, i) => {
            if (point[$groupColumns[i]] !== attr) {match = false;}
          });
          return match;
        }),
      };
    })
    .sort((a, b) => b.points.length - a.points.length);
</script>

<div w-full>
  {#if $groupNames.length === 0}
    <Container>
      <div class="flex items-top justify-between w-full" slot="header">
        <h3 class="font-bold whitespace-nowrap mr-3">
          {`Candidate Group ${candidatesGroupNumber}`}
        </h3>
        <IconButton
          on:click={() => {
            selectAll(
              selected,
              dataPoints.map((d) => d[$canvasSpec.idColumn])
            );
          }}
        >
          <Fa icon={faCheckSquare} slot="icon" />
        </IconButton>
      </div>
      <div class="flex" slot="content">
        <SampleRowContainer {dataPoints} {selected} {canvasSpec} {tooltip} {storybook}/>
      </div>
    </Container>
  {:else}
    <Container>
      <div class="flex items-top justify-between w-full" slot="header">
        <h3 class="font-bold whitespace-nowrap mr-3">
          {`Candidate Group ${candidatesGroupNumber}`}
        </h3>
        <IconButton
          on:click={() => {
            selectAll(
              selected,
              dataPoints.map((d) => d[$canvasSpec.idColumn])
            );
          }}
        >
          <Fa icon={faCheckSquare} slot="icon" />
        </IconButton>
      </div>
      <div slot="content">
        {#each filteredPoints as group, i}
          {#if group.points.length !== 0}
            <div class="flex items-center">
              <h3 class="whitespace-nowrap italic">
                {group.attrs.join(' | ')}
              </h3>
            </div>
            <SampleRowContainer
              {defaultNumberShown}
              dataPoints={group.points}
              {canvasSpec}
              {selected}
              {tooltip}
              {storybook}
            />
          {/if}
        {/each}
      </div>
    </Container>
  {/if}
</div>
