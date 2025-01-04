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
  export let categories: string[];
  export let colorScale: string[];
</script>

<div
  class="absolute top-4 right-4 flex flex-col justify-items-end bg-lightgrey p-2 bg-opacity-90"
>
  {#each categories as category, i}
    <div class="flex items-center pb-1 justify-end">
      <p class="pr-2">{category}</p>
      <div class="h-2 w-2" style="background-color: {colorScale[i]};" />
    </div>
  {/each}
</div>
