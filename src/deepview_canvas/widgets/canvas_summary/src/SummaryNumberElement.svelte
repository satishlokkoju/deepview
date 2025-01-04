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
  import type { SummaryDataElement } from '@betterwithdata/canvas_viz';

  export let data: SummaryDataElement;
  export let name: string;
  export let editMode: boolean;
</script>

<div
  class="{editMode ? 'border border-button_outline ' : ''} flex p-2 m-1 rounded"
>
  <p class="font-bold mr-2">
    {name}:
  </p>
  <p>
    {data.toLocaleString()}
  </p>
</div>
