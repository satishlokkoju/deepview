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
  import HeaderButton from "./HeaderButton.svelte";
  import Promo from "./Promo.svelte";

  export let experiment: string | undefined = undefined;
  export let pages: string[] | undefined = undefined;
  export let selectedPage: string | undefined = undefined;
</script>

<nav class="p-2 pl-3 bg-black flex justify-between">
  <div class="flex items-center">
    <h2 class="text-2xl font-bold text-text-dark">Canvas</h2>
    {#if pages !== undefined}
      <div class="flex pl-12 overflow-auto">
        {#each pages as page}
          <HeaderButton
            selected={page === selectedPage}
            value={page}
            on:click
          />
        {/each}
      </div>
    {/if}
  </div>
  <div class="flex items-center pl-4">
    {#if experiment !== undefined}
      <h2 class="text-text-dark font-bold pr-4">
        {experiment}
      </h2>
    {/if}
    <Promo />
  </div>
</nav>
