<!-- For licensing see accompanying LICENSE file.
Copyright (C) 2023 betterwithdata Inc. All Rights Reserved. -->

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
    <span slot="text">Use Canvas</span>
  </IconButton>
</div>
