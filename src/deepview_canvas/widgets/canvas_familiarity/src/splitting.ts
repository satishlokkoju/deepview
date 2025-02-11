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


import type { ColumnTable } from 'arquero';

export function getUniqueValuesForStringColumnForFamiliarity(
  split: boolean,
  familiarityColumn: string,
  columnName: string,
  table: ColumnTable
): string[] {
    if (split) {
      // Tf splitting familiarity

      // DeepView doesn't compute for classes with less than 50 data points (by default)
      // Filter out these less than 50 data point classes 
      let tempFamilarityPoint = table.get(familiarityColumn, 0) // get first familarity point, get classes from it's columns
      let familarityClassesList = Object.keys(tempFamilarityPoint)
      return familarityClassesList as string[];
  } else {
    // if not splitting familiarity, default on load
    
    const unique = table.groupby(columnName).count();
    return unique.array(columnName) as string[];
  }
}

export function getSplitTable(
  columnValue: string,
  familiarityColumn: string,
  column: string,
  table: ColumnTable
): ColumnTable {
  let resultTable = table;
  resultTable = resultTable.derive({
    selectedFamiliarity: `d.${familiarityColumn}['${columnValue}']`,
  });
  // This only works for columns that contain one string for a metadata class.
  resultTable = resultTable.filter(`d.${column} == "${columnValue}"`);
  return resultTable;
}

export function getSplitTables(
  columnValue: string,
  familiarityColumn: string,
  column: string,
  tables: ColumnTable[]
): ColumnTable[] {
  return tables.map((table) => {
    return getSplitTable(columnValue, familiarityColumn, column, table);
  });
}
