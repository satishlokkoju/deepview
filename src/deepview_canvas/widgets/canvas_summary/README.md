# Canvas Summary Widget

A component that displays an overview of the provided dataset table.
To configure it, pass a list of `SummaryElement`.
One `SummaryElement` is defined as:

```
export interface SummaryElement {
    name: string;
    data: number | ChartData;
}
```

`ChartData` is defined as:

```
export interface ChartData {
    spec: VegaLiteSpec;
    data: Record<string, unknown>;
}
```

## Installation

```bash
pip install canvas_summary
```


## Usage

To learn how to use Canvas, see the [documentation](https://satishlokkoju.github.io/deepview/).
