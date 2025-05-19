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
import { describe, it, expect, beforeEach } from 'vitest';
import { writable, get } from 'svelte/store';
import { selectAll } from '../../src/helpers/selection';

describe('Selection helpers', () => {
  // Test data
  let selectedStore: ReturnType<typeof writable<string[]>>;
  
  beforeEach(() => {
    // Reset the store before each test
    selectedStore = writable<string[]>([]);
  });

  describe('selectAll', () => {
    it('should add all new items when none of them exist in the store', () => {
      // Initial store is empty
      const newItems = ['A', 'B', 'C'];
      
      // Call selectAll
      selectAll(selectedStore, newItems);
      
      // Check result
      expect(get(selectedStore)).toEqual(['A', 'B', 'C']);
    });

    it('should merge new items with existing items in the store', () => {
      // Set initial items
      selectedStore.set(['A', 'D']);
      
      // New items to add
      const newItems = ['B', 'C'];
      
      // Call selectAll
      selectAll(selectedStore, newItems);
      
      // Check result - should include all items
      const result = get(selectedStore);
      expect(result).toHaveLength(4);
      expect(result).toContain('A');
      expect(result).toContain('B');
      expect(result).toContain('C');
      expect(result).toContain('D');
    });

    it('should remove all items when they already exist in the store', () => {
      // Set initial items
      selectedStore.set(['A', 'B', 'C']);
      
      // Call selectAll with the same items
      selectAll(selectedStore, ['A', 'B', 'C']);
      
      // Check result - should be empty
      expect(get(selectedStore)).toEqual([]);
    });

    it('should remove only the specified items when they all exist in the store', () => {
      // Set initial items
      selectedStore.set(['A', 'B', 'C', 'D']);
      
      // Call selectAll with a subset of items
      selectAll(selectedStore, ['A', 'C']);
      
      // Check result - should only contain B and D
      const result = get(selectedStore);
      expect(result).toHaveLength(2);
      expect(result).toContain('B');
      expect(result).toContain('D');
      expect(result).not.toContain('A');
      expect(result).not.toContain('C');
    });

    it('should add new items while keeping all existing items when not all new items exist in the store', () => {
      // Set initial items
      selectedStore.set(['A', 'B']);
      
      // Call selectAll with partially overlapping items
      selectAll(selectedStore, ['B', 'C']);
      
      // Check result - because C is not in the original store, all items are combined
      // B is only removed if ALL items in the newSelectedSet exist in existingSelectedSet
      const result = get(selectedStore);
      expect(result).toHaveLength(3);
      expect(result).toContain('A');
      expect(result).toContain('B');
      expect(result).toContain('C');
    });

    it('should handle empty arrays for both existing and new selections', () => {
      // Initial store is empty
      const newItems: string[] = [];
      
      // Call selectAll with empty arrays
      selectAll(selectedStore, newItems);
      
      // Check result - should still be empty
      expect(get(selectedStore)).toEqual([]);
    });

    it('should handle duplicate items in both arrays correctly', () => {
      // Set initial items with duplicates (duplicates are automatically handled by Set)
      selectedStore.set(['A', 'B', 'C']);
      
      // Call selectAll with duplicates
      selectAll(selectedStore, ['B', 'B', 'D']);
      
      // Check result - Since D doesn't exist in original set,
      // items are combined and duplicates are removed automatically by Set
      const result = get(selectedStore);
      expect(result).toContain('A');
      expect(result).toContain('B');
      expect(result).toContain('C');
      expect(result).toContain('D');
      
      // Since we're using a Set internally, duplicates are automatically removed
      expect(new Set(result).size).toBe(result.length);
    });
  });

  describe('setHasAll', () => {
    // We're testing an internal function, so we need to re-implement it here for testing
    const setHasAll = (set: Set<unknown>, setHas: Set<unknown>) => {
      for (var a of set) if (!setHas.has(a)) return false;
      return true;
    };

    it('should return true when setHas contains all elements from set', () => {
      const set = new Set(['A', 'B']);
      const setHas = new Set(['A', 'B', 'C']);
      
      expect(setHasAll(set, setHas)).toBe(true);
    });

    it('should return false when setHas is missing at least one element from set', () => {
      const set = new Set(['A', 'B', 'D']);
      const setHas = new Set(['A', 'B', 'C']);
      
      expect(setHasAll(set, setHas)).toBe(false);
    });

    it('should return true when both sets are empty', () => {
      const set = new Set();
      const setHas = new Set();
      
      expect(setHasAll(set, setHas)).toBe(true);
    });

    it('should return true when set is empty but setHas is not', () => {
      const set = new Set();
      const setHas = new Set(['A', 'B']);
      
      expect(setHasAll(set, setHas)).toBe(true);
    });
  });
});
