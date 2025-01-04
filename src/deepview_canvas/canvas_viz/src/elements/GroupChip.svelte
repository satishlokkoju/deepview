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
  import Icon from "svelte-fa";
  import { faTimes } from "@fortawesome/free-solid-svg-icons/faTimes";
  import { createEventDispatcher } from "svelte";

  export let values: string[];
  export let groupSize: number;

  const dispatch = createEventDispatcher();
</script>

<div
  class="flex items-center m-1 px-2 h-8 w-max border border-button_outline rounded {groupSize >
  0
    ? 'bg-body-light'
    : ''}"
>
  <div class="flex h-full pr-0.5 pl-0.5 items-center">
    {#each values as value, i}
      <div class="text-s pr-0.5 pl-0.5 font-normal max-w-full flex-initial">
        {value}
        {i !== values.length - 1 ? "|" : ""}
      </div>
    {/each}
  </div>
  <div class="text-s text-text-dimmed pr-0.5 pl-0.5">
    ({groupSize.toLocaleString()})
  </div>
  <div class="flex flex-auto pl-1 text-s">
    <button on:click={() => {
        dispatch("remove", { values: values })
        values = [] // clear the value list
      }}>
      <Icon icon={faTimes} />
    </button>
  </div>
</div>
