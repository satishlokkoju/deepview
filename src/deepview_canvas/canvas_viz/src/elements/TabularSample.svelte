<!-- For licensing see accompanying LICENSE file.
Copyright (C) 2023 betterwithdata Inc. All Rights Reserved. -->

<script lang="ts">
  import Fa from "svelte-fa";
  import { faTable } from "@fortawesome/free-solid-svg-icons/faTable";
  export let storybook: boolean = false;
</script>

<div class="p-2" on:click>
  <Fa icon={faTable} />
</div>
