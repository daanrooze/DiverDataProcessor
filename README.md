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
from DiverDataProcessor import read_td_diver, Geology, ObservationWell

# Load diver data from a CSV file
diver_data = read_td_diver("path/to/diver_data.csv")

# Define an observation well with relevant parameters
observation_well = ObservationWell(
    name="Example Well",          # Name of the well
    diver_code="XX11",            # Diver identifier
    surface_level=1.0,            # Surface level relative to vertical datu (in meters)
    top_well_to_sl=0.05,          # Distance from the top of the well to the surface level (in meters)
    well_depth=3.0,               # Total depth of the well (in meters)
    cable_length=1.5              # Length of the cable from the top of the well to the diver (in meters)
)

# Define geological layers for the observation well
geology = Geology(
    tops=[1.0, -2.0, -4.0],       # Top boundaries of geological layers (in meters)
    bottoms=[-2.0, -4.0, -6.0],   # Bottom boundaries of geological layers (in meters)
    lithology=["sand", "clay", "peat"],  # Lithology types for each layer
    surface_level=1.0             # Surface level relative to vertical datum (in meters)
)
```


### Processing

Provides tools to process and compensate diver pressure measurements for barometric pressure and adjust them relative to a vertical reference datum. Use the `processing.baro_compensate` function, which supports two methods for referencing to a vertical datum:

- **"handreading"**: Utilizes manual handreading data to calculate the diver's position relative to the datum. Use `DiverDataProcessor.HandReading` to supply the handreading data.
- **"cable"**: Uses the predefined diver distance from the top of the observation well. This is the default method.

In both cases, the height of the top of the well relative to the vertical datum must be known.

### Figures

Includes a template (`figures.GeologyGroundwater`) for creating a figure that displays groundwater levels in relation to geology. Optionally, precipitation bars can be added to the figure.

**Example:**

```python
from DiverDataProcessor import figures

# Create a GeologyGroundwater figure
fig = figures.GeologyGroundwater(observation_well, *kwargs)

# Plot the geological layers
fig.plot_geology()

# Plot the groundwater levels
fig.plot_water_level()

# Optionally, add precipitation bars to the figure
fig.plot_precipitation()
```
```


