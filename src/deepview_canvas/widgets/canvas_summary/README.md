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

To learn how to use Canvas, see the [documentation](https://betterwithdata.github.io/ml-Canvas/).

## Development

To learn about how to build Canvas from source and how to contribute to the framework, please look at [CONTRIBUTING.md](../CONTRIBUTING.md) and the [development documentation](https://betterwithdata.github.io/ml-Canvas/contributing.html).
