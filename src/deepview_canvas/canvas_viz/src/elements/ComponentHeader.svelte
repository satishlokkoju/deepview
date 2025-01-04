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
  import Heading from "./Heading.svelte";
  import IconButton from "./IconButton.svelte";

  import { exportView } from "../helpers/export";

  import Fa from "svelte-fa";
  import { faImage } from "@fortawesome/free-solid-svg-icons/faImage";

  export let title: string;
  export let description: string;
  export let container: HTMLDivElement;
</script>

<div class="flex items-top justify-between">
  <div class="flex flex-wrap">
    <Heading heading={title} {description} />
    <div class="flex flex-wrap">
      <slot />
    </div>
  </div>
  <div class="pb-3 pl-3">
    <IconButton on:click={() => exportView(container, "Scatterplot")}>
      <Fa icon={faImage} slot="icon" />
      <span slot="text">Download</span>
    </IconButton>
  </div>
</div>
