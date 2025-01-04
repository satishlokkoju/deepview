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
  import type { Writable } from 'svelte/store';
  import type { CanvasSpec } from '@betterwithdata/canvas_viz';

  import { SubHeading, ToggleButton, NumberInput } from '@betterwithdata/canvas_viz';

  export let canvasSpec: Writable<CanvasSpec>;

  let showUnfilteredData = $canvasSpec.showUnfilteredData;
  let instancesPerPage = $canvasSpec.instancesPerPage;

  $: canvasSpec.update((spec) => {
    spec.showUnfilteredData = showUnfilteredData;
    spec.instancesPerPage = instancesPerPage;
    return { ...spec };
  });
</script>

<div class="flex flex-col">
  <div class="px-2 pt-2">
    <SubHeading heading={'Settings'} />
  </div>
  <div class="p-2 flex flex-col">
    <ToggleButton
      title="Show unfiltered charts"
      bind:active={showUnfilteredData}
    />
    <div class="pt-1">
      <NumberInput title="Samples per page" bind:value={instancesPerPage} />
    </div>
  </div>
</div>
