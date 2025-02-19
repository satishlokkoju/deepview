/**
 * Copyright 2024 BetterWithData
 * 
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 * 
 *     http://www.apache.org/licenses/LICENSE-2.0
 * 
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License. 
 */

import { get, Writable } from "svelte/store";

export function selectAll(selectedStore: Writable<string[]>, newSelected: string[]) {
  let existingSelectedSet = new Set(get(selectedStore));
  let newSelectedSet = new Set(newSelected);

  if (setHasAll(newSelectedSet, existingSelectedSet)) {
    for (var toRemove of newSelectedSet) existingSelectedSet.delete(toRemove);
    selectedStore.update(() => [...existingSelectedSet]);
    return;
  }

  let combinedSelected = new Set([...existingSelectedSet, ...newSelectedSet]);
  selectedStore.set(Array.from(combinedSelected));
}

function setHasAll(set: Set<unknown>, setHas: Set<unknown>) {
  for (var a of set) if (!setHas.has(a)) return false;
  return true;
}
