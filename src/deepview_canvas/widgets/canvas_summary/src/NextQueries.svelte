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
  import type { QueryElement } from '@betterwithdata/canvas_viz';

  import Fa from 'svelte-fa';
  import { createEventDispatcher } from 'svelte';
  import { fade } from 'svelte/transition';

  export let currentQuery: QueryElement;

  $: nextQueries = currentQuery.next as QueryElement[];

  const dispatch = createEventDispatcher();

  function querySelected(query: QueryElement) {
    dispatch('querySelected', { query: query });
  }
</script>

<div class="flex flex-wrap" transition:fade>
  {#each nextQueries as query}
    <div
      class="flex flex-grow justify-center items-center m-1 p-1 border border-midgrey rounded cursor-pointer"
      on:click={() => querySelected(query)}
    >
      {#if query.icon !== undefined}
        <Fa color="#7f7f7f" icon={query.icon} />
      {/if}
      <span class="pl-1 text-darkgrey">{query.name}</span>
    </div>
  {/each}
</div>
