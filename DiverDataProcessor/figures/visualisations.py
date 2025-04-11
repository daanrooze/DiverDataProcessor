import contextily as cx
import geopandas as gpd
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import xarray as xr
from matplotlib.gridspec import GridSpec

from DiverDataProcessor import base

DATE_FORMAT = mdates.DateFormatter("%m/%Y")


class LithologyColormap:
    fill = "grey"
    clay = "#009200"
    sandy_clay = "#078C03"
    clay_loam = "#367C2C"
    sandy_loam = "#B2EC5E"
    loamy_sand = "#DAE95D"
    sand = "#F2E205"


class VariableColormap:
    water_level = "#141E95"
    salinity = "#861657"
    temperature = "#26D39E"
    precipitation = "#861657"


class GeologyGroundwater:
    def __init__(self, observation_well: base.ObservationWell, **figure_kwargs):
        """
        Create figure with geology (left) and groundwater level (right).

        Parameters
        ----------
        observation_well : base.ObservationWell
            The observation well object containing data to be visualized.
        **figure_kwargs : dict
            Additional keyword arguments to customize the matplotlib figure.
        Attributes
        ----------
        fig : matplotlib.figure.Figure
            The main figure object for the visualisation.
        geology : matplotlib.axes._subplots.AxesSubplot
            The subplot for displaying geological data.
        water_level : matplotlib.axes._subplots.AxesSubplot
            The subplot for displaying water level data.
        precipitation : matplotlib.axes._subplots.AxesSubplot
            (optional) The twin subplot for displaying precipitation data.
        """
        self.fig = plt.figure(**figure_kwargs)
        width_ratios = [0.2, 1.0]
        wspace = 0.35
        gs = GridSpec(
            nrows=1, ncols=2, figure=self.fig, width_ratios=width_ratios, wspace=wspace
        )

        self.geology = self.fig.add_subplot(gs[0])
        self.water_level = self.fig.add_subplot(gs[1])
        self.precipitation = self.water_level.twinx()
        self.fig.suptitle(observation_well.name)

    def _hide_precipitation_axis(self):
        self.precipitation.spines["top"].set_visible(False)
        self.precipitation.spines["bottom"].set_visible(False)
        self.precipitation.spines["right"].set_visible(False)
        self.precipitation.set_ylabel("")
        self.precipitation.tick_params(axis="y", colors="none")

    def _show_precipitation_axis(self):
        self.precipitation.spines["right"].set_visible(True)
        self.precipitation.spines["right"].set_color(VariableColormap.precipitation)
        self.precipitation.tick_params(axis="y", colors=VariableColormap.precipitation)
        self.precipitation.set_ylabel(
            "Neerslag [mm]", color=VariableColormap.precipitation
        )

    def plot_geology(self, geology: base.Geology, units: str):
        bottoms = geology.bottoms
        thickness = geology.thickness
        lithology = geology.lithology
        bottom = bottoms[-1]
        surface_level = bottom + sum(thickness)

        colors = []
        for lith in lithology:
            colors.append(getattr(LithologyColormap, lith))

        self.geology.bar([1], height=thickness, bottom=bottoms, color=colors, width=0.8)
        self.geology.set_ylabel(f"Geologie [{units}]")
        self.geology.xaxis.set_ticks([])
        self.geology.spines["top"].set_visible(False)
        self.geology.spines["bottom"].set_visible(False)
        self.geology.spines["right"].set_visible(False)
        self.geology.set_ylim(bottom, surface_level + 0.20)

    def plot_water_level(self, water_level: pd.Series, units: str):
        x = water_level.index
        y1 = water_level.values
        y2 = np.nanmin(y1) - 30.0

        self.water_level.plot(x, y1, color=VariableColormap.water_level)
        self.water_level.fill_between(
            x, y1=y1, y2=y2, color=VariableColormap.water_level, alpha=0.1
        )
        self.water_level.spines["top"].set_visible(False)
        self.water_level.spines["right"].set_visible(False)
        self.water_level.margins(x=0)
        self.water_level.xaxis.set_major_formatter(DATE_FORMAT)
        self.water_level.xaxis.set_major_locator(mdates.MonthLocator())
        self.water_level.tick_params(axis="x", rotation=45)
        self.water_level.set_ylabel(f"Grondwaterstand [{units}]")
        #
        ymin, ymax = self.geology.get_ylim()
        self.water_level.set_ylim(ymin, ymax)
        #
        self._hide_precipitation_axis()

    def plot_precipitation(self, precipitation: pd.Series):
        x = precipitation.index
        y = precipitation.values

        self.precipitation.bar(x, y, color=VariableColormap.precipitation)
        self.precipitation.margins(x=0)
        self.precipitation.set_ylim([0, 100])

        self._show_precipitation_axis()
