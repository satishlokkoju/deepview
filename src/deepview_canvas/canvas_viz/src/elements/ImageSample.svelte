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
  import type { CanvasSpec } from "../types";
  import type { Writable } from "svelte/store";
  import { join } from "@fireflysemantics/join";

  import { ContentsService } from '../helpers/contentservice';

  export let id: string;
  export let canvasSpec: Writable<CanvasSpec>;
  export let large: boolean = false;
  export let storybook: boolean = false;

  let imagePromise: Promise<string>;

  $:imagePromise = loadImage($canvasSpec.filesPath, id);

  const contentsManager = ContentsService.getInstance();

  async function loadImage(filesPath: string, imageId: string): Promise<string> {
    if (storybook) {
      return join(filesPath, imageId);
    } else {
      try {
        const filePath = join(filesPath, imageId);
        const result = await contentsManager.readContent(filePath);
        
        if (typeof result !== 'string') {
          throw new Error('Unexpected content type');
        }
        return result;
      } catch (error) {
        console.error('Error reading image file:', error);
        throw new Error(`Failed to load image: ${imageId}`);
      }
    }
  }

  function handleImageError(event: Event) {
    console.error("Error loading image:", event);
    const target = event.target as HTMLImageElement;
    target.alt = 'Image failed to load';
  }
</script>

<div>
  {#await imagePromise}
    <p class="loading">Loading...</p>
  {:then src}
  <img id = "imageSample"
    {src}
    alt={"Image with title: " + id}
    class={large ? "mx-1" : "w-12 m-1"}
    style={`background: black; max-width: ${large ? '256px' : '128px'}`}
    on:error={handleImageError}
  />
  {:catch error}
    <p class="error">{error.message}</p>
  {/await}

</div>
