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
  export let active: boolean = true;
  export let title: string;
</script>

<button
  type="button"
  class="flex justify-between items-center w-full"
  on:click={() => (active = !active)}
  on:keydown={(e) => {
    if (e.key === 'Enter' || e.key === ' ') {
      active = !active;
      e.preventDefault();
    }
  }}
  aria-pressed={active}
  aria-label={title}
>
  <span class="pr-1">{title}</span>
  <div
    class="w-10 h-6 flex items-center bg-midgrey rounded-full p-1 duration-100 ease-in-out {active
      ? 'bg-highlight'
      : ''}"
    aria-hidden="true"
  >
    <div
      class="bg-white w-4 h-4 rounded-full shadow-md transform duration-100 ease-in-out {active
        ? 'translate-x-4'
        : ''}"
      aria-hidden="true"
    />
  </div>
</button>
