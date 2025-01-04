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

import type ColumnTable from "arquero/dist/types/table/column-table";

const UNIQUE_COLS_PCTG = 0.1;

export function getColumnType(
  table: ColumnTable,
  columnName: string
): string | undefined {
  const col = table.column(columnName);
  if (col === undefined) {
    return undefined;
  }
  const firstValue = col.get(0);
  if (firstValue.constructor.name === "SignedBigNum") {
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
  const colNames = table.columnNames();
  const binnnableStringColumns: string[] = [];
  for (const colName of colNames) {
    const columnType = getColumnType(table, colName);
    if (columnType === "string") {
      if (isStringColumnBinnable(colName, table)) {
        binnnableStringColumns.push(colName);
      }
    }
  }
  return binnnableStringColumns;
}

export function isStringColumnBinnable(
  columnName: string,
  table: ColumnTable
): boolean {
  /** If more than UNIQUE_COLS_PCTG percent of the column are unique strings, likely an ID, don't bin. */
  const unique = table.groupby(columnName).count().numRows();
  if (unique < UNIQUE_COLS_PCTG * table.numRows()) {
    return true;
  }
  return false;
}

export const cartesian = (...a: string[][]): string[] =>
  a.reduce((a, b) =>
    a.flatMap((d) =>
      b.map((e: any) => [d, e].reduce((acc, val) => acc.concat(val), []))
    )
  );
