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


import type {
  CanvasSpec,
  TooltipSpec,
  WidgetSpec,
  SummaryWidgetSpec,
} from "./types";
import type { DOMWidgetModel } from "@jupyter-widgets/base";
import type { Writable, Readable, Updater } from "svelte/store";

import { ColumnTable, fromArrow, op } from "arquero";
import { writable, derived, get } from "svelte/store";
import { cartesian } from "./helpers/table";


/**
 * Adapted from https://github.com/cabreraalex/widget-svelte-cookiecutter
 *
 * @param name_ Name of the variable in the model. This is the same as the
 *              name of the corresponding Python variable in widget.py
 * @param value_ Default value
 * @param model backbone model containing state synced between Python and JS
 * @returns Svelte store that is synced with the model.
 */
export function createSyncedWidget<T>(
  name_: string,
  value_: T,
  model: DOMWidgetModel
): Writable<T> {
  const name: string = name_;
  const internalWritable: Writable<T> = writable(value_);

  const modelValue = model.get(name);
  if (modelValue !== undefined && modelValue !== null) {
    internalWritable.set(modelValue);
  }

  // when the model changes, update the store
  model.on('change:' + name, () => internalWritable.set(model.get(name)), null);

  return {
    // when the store changes, update the model
    set: (v: T) => {
      internalWritable.set(v);
      if (model) {
        model.set(name, v);
        model.save_changes();
      }
    },
    subscribe: internalWritable.subscribe,
    update: (func: (v: T) => T) => {
      internalWritable.update((v: T) => {
        const output = func(v);
        if (model) {
          model.set(name, output);
          model.save_changes();
        }
        return output;
      });
    },
  };
}

export let canvasSpec: Writable<CanvasSpec>;
export let widgetSpecs: Writable<Record<string, WidgetSpec | SummaryWidgetSpec>>;
export let dataTable: Writable<DataView>;
export let selected: Writable<string[]>;
export let groupColumns: Writable<string[]>;
export let filter: Writable<string>;
export let filterError: Writable<string>;
export let tooltip: Writable<TooltipSpec>;

export let table: Readable<ColumnTable>;
export let filteredTable: Readable<ColumnTable>;
export let groupNames: Readable<string[] | string[][]>;
export let groupedTables: Readable<ColumnTable[]>;


/**
 * https://github.com/NicolaZucchia/WorkingVisLabTool/blob/main/src/stores.ts
 * Note that when the cell containing the widget is re-run, a new model is
 * created. We don't want the former model to hang around. We don't want state
 * to carry over when the widget is re-run. That's why all of the stores are
 * initialized in this function, which is called when the widget's cell is run.
 * @param model backbone model that contains state synced between Python and JS
 */
export function initializeStores(model: DOMWidgetModel): void {
  canvasSpec = createSyncedWidget<CanvasSpec>(
    "canvas_spec",
    {} as CanvasSpec,
    model
  );

  widgetSpecs = createSyncedWidget<Record<string, WidgetSpec | SummaryWidgetSpec>>("widgetSpecs", {}, model);

  dataTable = createSyncedWidget<DataView>(
    "table",
    new DataView(new ArrayBuffer(0)),
    model
  );

  selected = createSyncedWidget<string[]>("selected", [], model);

  groupColumns = createSyncedWidget<string[]>("group_columns", [], model);
  filter = createSyncedWidget<string>("filter", "", model);
  filterError = createSyncedWidget<string>("filter_error", "", model);

  tooltip = createSyncedWidget<TooltipSpec>(
    "data_sample_tooltip",
    {
      hover: false,
      mousePos: { x: 0, y: 0 },
      fetchPrefix: "",
      instance: undefined,
      number: 0,
    },
    model
  );

  table = derived(dataTable, (d: DataView) => fromArrow(d.buffer));

  filteredTable = derived(
    [table, filter],
    ([table, filter]) => {
      filterError.set("");
      let filteredTable = table;
      if (filter) {
        try {
          filteredTable = filteredTable.filter(filter);
        } catch (err) {
          filterError.set(err as string);
        }
      }
      return filteredTable;
    }
  );

  groupNames = derived(
    [filteredTable, groupColumns],
    ([filteredTable, groupColumns]) => {
      if (groupColumns.length > 0) {
        const uniqueColumnValues: string[][] = groupColumns.map(
          (col) =>
          (
            filteredTable
              .rollup({ col: op.array_agg_distinct(col) })
              .object() as any
          ).col
      );
      // If just one column, don't do cartesian product and make it a 2D array.
      if (uniqueColumnValues.length === 1) {
        return uniqueColumnValues[0].map((group) => [group]);
      }
      return cartesian(...uniqueColumnValues);
    } else return [];
  }
);

groupedTables = derived( [filteredTable, groupColumns, groupNames, canvasSpec], ([filteredTable, groupColumns, groupNames, canvasSpec]) => {
      if (
        groupColumns !== undefined &&
        filteredTable !== undefined &&
        groupNames !== undefined &&
        groupColumns.length > 0 &&
        groupNames.length > 0
      ) {
        let groupedTable = filteredTable.groupby(...groupColumns);
        let partitions = groupedTable.partitions();

        let groupedTables: ColumnTable[] = partitions.map((partition) =>
          filteredTable.reify(Array.from(partition))
        );
        return groupedTables;
      } else {
        return [];
      }
    }
  );
}
