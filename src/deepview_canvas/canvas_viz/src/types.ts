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


import type { DOMWidgetModel } from "@jupyter-widgets/base";
import type { ColumnTable } from "arquero";
import type { VegaLiteSpec, VegaSpec } from "svelte-vega";
import type { IconDefinition } from "@fortawesome/fontawesome-common-types";
import type { Writable } from "svelte/store";

export enum CanvasDataType {
  TABULAR = 1,
  IMAGE = 2,
  AUDIO = 3,
}

export enum ResolverType {
  BINNED_STRING,
  NUMBER,
}

export interface CanvasSpec {
  filesPath: string;
  idColumn: string;
  dataType: CanvasDataType;
  instancesPerPage: number;
  showUnfilteredData: boolean;
}

export interface WidgetSpec {
  width: string;
  height: string;
  page: string;
  name: string;
  description: string;
}

export interface ClassificationSpec extends WidgetSpec {
  labelColumn: string;
  predictionColumn: string;
}

export interface VegaWidgetSpec extends WidgetSpec {
  vegaElements: (VegaSpec | VegaLiteSpec)[];
}

export interface SummaryWidgetSpec extends WidgetSpec {
  summaryElements: SummaryElement[];
}

export interface MarkdownSpec extends WidgetSpec {
  content: string;
  title: string;
}

export interface DataMapSpec extends WidgetSpec {
  projection: string;
  idMap: Record<string, number>;
  feature: string;
  idColumn: string;
  mapUrl: string;
}

export interface SummaryElement {
  name: string;
  data: number | ChartData;
}

export interface ChartDataResolver {
  type: ResolverType;
  columnName: string;
}

export interface ChartData {
  spec: VegaLiteSpec;
  data: Record<string, unknown>;
  resolver?: ChartDataResolver;
}

export interface TooltipSpec {
  hover: boolean;
  mousePos: { x: number; y: number };
  fetchPrefix: string;
  instance?: Record<string, unknown>;
  number?: number;
}

export interface SummaryData {
  rows: SummaryRow[];
}

export interface SummaryRow {
  name: string;
  data: SummaryDataElement;
}

export interface ChartData {
  spec: VegaLiteSpec;
  data: Record<string, unknown>;
}

export type SummaryDataElement = number | ChartData;

export interface WidgetInfo {
  experiment: string;
  pages: Pages;
  spec: CanvasSpec;
  exportID: string;
}

export interface Pages {
  [name: string]: Widget[];
}

export interface Widget {
  name: string;
  width: string;
  height: string;
  page: string;
  spec: WidgetSpec | SummaryWidgetSpec;
}

export interface QueryElement {
  name: string;
  icon?: IconDefinition;
  next?: QueryElement[] | QueryResolver;
}

export type QueryResolver = (
  names: string[],
  table: ColumnTable
) => SummaryElement | undefined;

export interface WidgetWritable<T> extends Writable<T> {
  setModel: (m: DOMWidgetModel) => void;
}

export interface ConfusionMatrixEntry {
  tp: number;
  tn: number;
  fp: number;
  fn: number;
  acc: number;
  size: number;
}
