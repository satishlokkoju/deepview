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
import type { ColumnTable } from "arquero";

const UNIQUE_COLS_PCTG = 0.1;

export function getColumnType(
  table: ColumnTable,
  columnName: string
): string | undefined {
  // Check if column exists
  if (!table.column(columnName)) {
    return undefined;
  }

  // Get the first value using array() method
  const columnValues = table.array(columnName);
  const firstValue = columnValues[0];

  // Handle special case for SignedBigNum (often used for large numbers in Arquero)
  if (firstValue?.constructor.name === "SignedBigNum") {
    return "number";
  }
  if (typeof firstValue === "object") {
    const objectClass: string = firstValue.constructor.name;
    if (objectClass.includes("Array")) {
      return "array";
    }
  }
  return typeof firstValue;
}

export function getBinnableStringColumns(table: ColumnTable): string[] {
  if (!table) {
    console.warn("[table] getBinnableStringColumns: Table is null or undefined");
    return [];
  }

  try {
    const colNames = table.columnNames();
    const binnnableStringColumns: string[] = [];
    
    // Process in batches for large tables to avoid UI freezing
    const processColumns = (startIdx: number, batchSize: number) => {
      const endIdx = Math.min(startIdx + batchSize, colNames.length);
      
      for (let i = startIdx; i < endIdx; i++) {
        const colName = colNames[i];
        try {
          const columnType = getColumnType(table, colName);
          if (columnType === "string") {
            try {
              if (isStringColumnBinnable(colName, table)) {
                binnnableStringColumns.push(colName);
              }
            } catch (error) {
              console.warn(`[table] Error checking if column ${colName} is binnable:`, error);
            }
          }
        } catch (error) {
          console.warn(`[table] Error processing column ${colName}:`, error);
        }
      }
      
      // If there are more columns to process, schedule the next batch
      if (endIdx < colNames.length) {
        setTimeout(() => processColumns(endIdx, batchSize), 0);
      }
    };
    
    // For smaller tables, process all at once
    if (colNames.length <= 20) {
      processColumns(0, colNames.length);
    } else {
      // For larger tables, process in smaller batches
      processColumns(0, 20);
    }
    
    return binnnableStringColumns;
  } catch (error) {
    console.error("[table] getBinnableStringColumns: Error processing table:", error);
    return [];
  }
}

export function isStringColumnBinnable(
  columnName: string,
  table: ColumnTable
): boolean {
  /** If more than UNIQUE_COLS_PCTG percent of the column are unique strings, likely an ID, don't bin. */
  const threshold = Math.ceil(UNIQUE_COLS_PCTG * table.numRows());
  
  // Early optimization: if we have fewer rows than threshold, we can use the original approach
  if (table.numRows() <= threshold) {
    const unique = table.groupby(columnName).count().numRows();
    return unique < threshold;
  }
  
  // More memory-efficient approach for larger tables
  const uniqueValues = new Set<string>();
  const column = table.array(columnName);
  
  // Only need to check until we exceed threshold
  for (let i = 0; i < column.length; i++) {
    const value = column[i]?.toString() || '';
    uniqueValues.add(value);
    
    // If we've already found more unique values than our threshold,
    // we can stop early and return false
    if (uniqueValues.size >= threshold) {
      return false;
    }
  }
  
  return true;
}

export const cartesian = (...a: string[][]): string[] =>
  a.reduce((a, b) =>
    a.flatMap((d) =>
      b.map((e: any) => [d, e].reduce((acc, val) => acc.concat(val), []))
    )
  );
