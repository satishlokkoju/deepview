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
  import type { QueryElement } from '@betterwithdata/canvas_viz';

  import { createEventDispatcher } from 'svelte';
  import { fade } from 'svelte/transition';

  import SelectedQueries from './SelectedQueries.svelte';
  import NextQueries from './NextQueries.svelte';
  import { getQueryTree } from './summarySpecs';

  import type { ColumnTable } from 'arquero';

  export let table: ColumnTable;

  const dispatch = createEventDispatcher();
  let selectedQueries: QueryElement[] = [];
  let currentQuery: QueryElement = getQueryTree(table);

  function querySelected(event: CustomEvent) {
    const query = event.detail.query as QueryElement;
    if (typeof query.next === 'function') {
      dispatch('elementSelected', {
        element: query.next(
          selectedQueries.map((query) => query.name),
          table
        ),
      });
      currentQuery = getQueryTree(table);
      selectedQueries = [];
    } else {
      selectedQueries = [...selectedQueries, query];
      currentQuery = query;
    }
  }

  function previousQuery(event: CustomEvent) {
    const previousQuery = event.detail.query as QueryElement;
    const index = selectedQueries.findIndex((query) => query === previousQuery);
    if (index === 0) {
      currentQuery = getQueryTree(table);
      selectedQueries = [];
    } else {
      currentQuery = selectedQueries[index - 1];
      selectedQueries.slice(index - 1);
    }
  }
</script>

<div
  class="flex flex-col p-2 bg-lightgrey border-midgrey border-2 rounded select-none"
  transition:fade
>
  <div class="flex flex-col">
    <SelectedQueries {selectedQueries} on:previousQuery={previousQuery} />
    <NextQueries {currentQuery} on:querySelected={querySelected} />
  </div>
</div>
