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
  import Tooltip from "./Tooltip.svelte";

  export let heading: string;
  export let description: string;

  let hover = false;
  let offsetX = 0;
</script>

<div class="flex items-center justify-between pb-3 pr-4">
  <div class="flex items-center">
    <h2 class="text-2xl font-bold leading-7 text-gray-900 pr-2">
      {heading}
    </h2>
    <Tooltip text={description} />
  </div>
</div>
