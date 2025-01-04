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


export function mapWidth(width: string): string {
  switch (width) {
    case 'XS':
      return 'col-span-1';
    case 'S':
      return 'col-span-2';
    case 'M':
      return 'col-span-3';
    case 'L':
      return 'col-span-4';
    case 'XL':
      return 'col-span-5';
    case 'XXL':
      return 'col-span-6';
    default:
      return 'col-span-2';
  }
}

export function mapHeight(height: string, grid = false): string {
  switch (height) {
    case 'XS':
      return grid ? 'row-span-1' : 'max-h-XS';
    case 'S':
      return grid ? 'row-span-2' : 'max-h-S';
    case 'M':
      return grid ? 'row-span-3' : 'max-h-M';
    case 'L':
      return grid ? 'row-span-4' : 'max-h-L';
    case 'XL':
      return grid ? 'row-span-5' : 'max-h-XL';
    case 'XXL':
      return grid ? 'row-span-6' : 'max-h-XXL';
    default:
      return grid ? 'row-span-2' : 'max-h-S';
  }
}

export function mapHeightFixed(height: string, grid = false): string {
  switch (height) {
    case 'XS':
      return grid ? 'row-span-1' : 'h-XS';
    case 'S':
      return grid ? 'row-span-2' : 'h-S';
    case 'M':
      return grid ? 'row-span-3' : 'h-M';
    case 'L':
      return grid ? 'row-span-4' : 'h-L';
    case 'XL':
      return grid ? 'row-span-5' : 'h-XL';
    case 'XXL':
      return grid ? 'row-span-6' : 'h-XXL';
    default:
      return grid ? 'row-span-2' : 'h-S';
  }
}
