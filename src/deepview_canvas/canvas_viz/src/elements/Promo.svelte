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


<script>
  import Fa from "svelte-fa";
  import { faGithub } from "@fortawesome/free-brands-svg-icons/faGithub";

  import IconButton from "./IconButton.svelte";
</script>

<div>
  <IconButton
    on:click={() =>
      window.open("https://github.com/satishlokkoju/deepview", "_blank")}
    filled={true}
  >
    <Fa icon={faGithub} slot="icon" />
    <span slot="text">Use DeepView Canvas</span>
  </IconButton>
</div>
