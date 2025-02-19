<!-- Copyright 2024 BetterWithData

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License. -->

<script lang="ts">
  import Fa from "svelte-fa";
  import { faTable } from "@fortawesome/free-solid-svg-icons/faTable";
  import { faSort } from "@fortawesome/free-solid-svg-icons/faSort";
  import { faSortUp } from "@fortawesome/free-solid-svg-icons/faSortUp";
  import { faSortDown } from "@fortawesome/free-solid-svg-icons/faSortDown";

  export let data: Record<string, unknown>[] = [];
  export let maxRows = 10;

  let sortField: string | null = null;
  let sortDirection: 'asc' | 'desc' = 'asc';
  
  $: columns = data.length > 0 ? Object.keys(data[0]) : [];
  $: sortedData = [...data].sort((a, b) => {
    if (!sortField) return 0;
    const aVal = a[sortField];
    const bVal = b[sortField];
    const direction = sortDirection === 'asc' ? 1 : -1;
    if (aVal < bVal) return -1 * direction;
    if (aVal > bVal) return 1 * direction;
    return 0;
  }).slice(0, maxRows);

  function toggleSort(column: string) {
    if (sortField === column) {
      sortDirection = sortDirection === 'asc' ? 'desc' : 'asc';
    } else {
      sortField = column;
      sortDirection = 'asc';
    }
  }

  function getSortIcon(column: string) {
    if (sortField !== column) return faSort;
    return sortDirection === 'asc' ? faSortUp : faSortDown;
  }
</script>

{#if data.length === 0}
  <div class="p-2 text-gray-500 flex items-center justify-center border rounded-lg">
    <Fa icon={faTable} />
    <span class="ml-2">No data available</span>
  </div>
{:else}
  <div class="overflow-x-auto border rounded-lg shadow-sm">
    <table class="min-w-full divide-y divide-gray-300">
      <thead class="header-bg">
        <tr>
          {#each columns as column}
            <th 
              class="px-6 py-3 text-left text-xs font-bold text-white uppercase tracking-wider cursor-pointer hover-header border-r last:border-r-0"
              on:click={() => toggleSort(column)}
            >
              <div class="flex items-center">
                {column}
                <span class="ml-2">
                  <Fa icon={getSortIcon(column)} size="sm" />
                </span>
              </div>
            </th>
          {/each}
        </tr>
      </thead>
      <tbody class="divide-y divide-gray-300">
        {#each sortedData as row, i}
          <tr class="{i % 2 === 0 ? 'even-row' : 'odd-row'}">
            {#each columns as column}
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900 border-r last:border-r-0">
                {row[column]}
              </td>
            {/each}
          </tr>
        {/each}
      </tbody>
    </table>
  </div>
{/if}

<style>
  table {
    border-collapse: collapse;
    width: 100%;
  }
  
  th, td {
    border-color: #d1d5db;
  }
  
  thead {
    border-bottom: 2px solid #d1d5db;
  }

  .header-bg {
    background-color: #1e3a8a;  /* Dark blue */
  }

  .hover-header:hover {
    background-color: #1e40af;  /* Slightly lighter blue for header hover */
  }

  .even-row {
    background-color: #e6f3ff;
  }

  .odd-row {
    background-color: #f0f7ff;
  }

  tr:hover {
    background-color: #cce4ff !important;
  }
</style>
