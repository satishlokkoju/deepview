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
  export let filled = false;
</script>

<button
  class="{filled
    ? 'bg-button hover:bg-button_hover text-text-dark'
    : 'bg-white text-button border border-button hover:bg-button hover:text-white'} rounded-md py-1 px-2 transition"
  on:click
  on:mouseleave
>
  <div class="flex items-center">
    {#if $$slots.icon}
      <div class={$$slots.text ? "pr-2 flex" : "flex"}>
        <slot name="icon" />
      </div>
    {/if}
    <slot name="text" />
  </div>
</button>
