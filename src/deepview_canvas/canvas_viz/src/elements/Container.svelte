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
  export let title: string | undefined = undefined;
  export let categories: string[] | undefined = undefined;
</script>

<div class="flex flex-col border-midgrey border rounded-md p-2 w-full">
  <div class="flex items-top mb-2 justify-between border-b pb-1 border-midgrey">
    <slot name="header" />
  </div>
  <div class="flex items-center">
    <slot name="icon" />
    {#if title !== undefined}
      <span class="pr-2 text-lg">{title}</span>
    {/if}
    {#if categories !== undefined}
      {#each categories as category}
        <span class="pr-1 text-sm">{category}</span>
      {/each}
    {/if}
  </div>
  <slot name="content" />
</div>
