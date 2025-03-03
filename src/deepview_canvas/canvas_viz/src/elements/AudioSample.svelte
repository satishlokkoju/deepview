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
  import { onDestroy } from "svelte";

  import { ContentsService } from '../helpers/contentservice';
  import WaveSurfer from "wavesurfer.js";
  import IconButton from "./IconButton.svelte";
  import { join } from "@fireflysemantics/join";

  import Fa from "svelte-fa";
  import { faPlay } from "@fortawesome/free-solid-svg-icons/faPlay";
  import { faPause } from "@fortawesome/free-solid-svg-icons/faPause";

  export let id: string;
  export let canvasSpec: Writable<CanvasSpec>;
  export let large: boolean = false;
  export let storybook: boolean = false;
  
  const contentsManager = ContentsService.getInstance();
  

  function base64ToArrayBuffer(base64: string): ArrayBuffer {
    try {
      const trimmedBase64 = base64.trim();
      const binaryString = atob(trimmedBase64);
      const bytes = new Uint8Array(binaryString.length);
      for (let i = 0; i < binaryString.length; i++) {
        bytes[i] = binaryString.charCodeAt(i);
      }
      return bytes.buffer;
    } catch (error) {
      console.error("Failed to decode base64 string:", error);
      console.log("Problematic base64 string:", base64);
      throw error;
    }
  }


  let container: HTMLElement;
  let wavesurfer: WaveSurfer;
  let playing: boolean = false;
  let oldId: string = "";

  $: if (container !== undefined && id !== oldId) {
    if (wavesurfer !== undefined) wavesurfer.destroy();
    container.innerHTML = "";
    wavesurfer = WaveSurfer.create({
      container: container,
      waveColor: "#cfcfcf",
      progressColor: "#0071e3",
    });

    const filePath = join($canvasSpec.filesPath, id);
    if (storybook) {
      wavesurfer.load(filePath);
    } else {
      contentsManager.readAudioContent(filePath).then(result => {
        const arrayBuffer = base64ToArrayBuffer(result);
        wavesurfer.loadArrayBuffer(arrayBuffer);
      }).catch(error => {
        console.error("Unable to load the audio data", error)
      });
    }

    playing = false;
    oldId = id;
  }

  function changePlayStatus() {
    if (playing) {
      wavesurfer.pause();
      playing = false;
    } else {
      wavesurfer.play();
      playing = true;
    }
  }

  onDestroy(() => {
    if (wavesurfer) {
      wavesurfer.destroy();
    }
  });
</script>

<div class="flex flex-col {large ? 'w-48 mx-1' : 'w-24 m-1'}">
  <button 
    bind:this={container} 
    on:click 
    type="button"
    class="p-0 border-0 bg-transparent"
  />
  <div>
    <IconButton on:click={changePlayStatus}>
      <Fa icon={playing ? faPause : faPlay} slot="icon" />
    </IconButton>
  </div>
</div>
