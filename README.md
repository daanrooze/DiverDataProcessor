# DiverDataProcessor

A Python package for processing and analyzing diver pressure logger data, generating time series and basic visualizations.

## Installation

To install using Pixi, run:

```bash
pixi install .
```

For more information about Pixi, visit: [https://pixi.sh/latest/](https://pixi.sh/latest/)

## Usage

### Base & Readers

Provides utilities to open diver data exported as CSV files from Diver Office and load them as `Timeseries` objects. This enables minor functionalities such as reindexing. Additionally, it includes a fixed format to handle observation wells, geology, and groundwater hand readings.

**Example:**

```python
DiverDataProcessor.read_td_diver(path_diver)
```

### Processing

Offers tools to process and analyze diver data efficiently.

