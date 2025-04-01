import pandas as pd

MBAR_TO_MH2O = 0.0101972


def remove_outliers(data: pd.DataFrame, threshold=3):
    mean = data.mean()
    std_dev = data.std()

    lower_bound = mean - threshold * std_dev
    upper_bound = mean + threshold * std_dev

    return data[~((data < lower_bound) | (data > upper_bound))]


class ObservationWell:
    """
    A class object to represent an observation well and its associated properties.

    Attributes:
    -----------
    name : str
        The name of the observation well.
    diver_code : str
        A code identifying the diver.
    surface_level : float
        The elevation of the surface level (m datum)
    top_well_to_sl : float
        Depth of top well to surface level (m).
    well_depth : float
        The total depth of the well (m).
    cable length : float
        The total length of the cable to the top well (m).
    """

    def __init__(
        self,
        name: str,
        diver_code: str,
        surface_level: float,
        top_well_to_sl: float,
        well_depth: float,
        cable_length: float = None,
    ):
        self.name = name
        self.diver_code = diver_code
        self.surface_level = surface_level
        self.top_well = surface_level - top_well_to_sl
        self.well_depth = well_depth
        if cable_length is not None:
            self.diver_to_datum = self.top_well - cable_length
        else:
            self.diver_to_datum = None


class HandReading:
    """
    A class to represent a hand reading taken at a specific time.

    Attributes:
    -----------
    datetime : pd.Timestamp
        The date and time of the hand reading format (Y-m-d H:M:S).
    reading : float
        Handreading below top of well in (m).
    """

    def __init__(self, datetime, reading):
        self.datetime = pd.to_datetime(datetime, format="%Y-%m-%d %H:%M:%S")
        self.reading = float(reading)


class Geology:
    def __init__(self, surface_level, tops, bottoms, lithology, unit="meters"):

        self.thickness = bottoms - tops
        self.bottoms = surface_level - bottoms
        self.tops = surface_level - tops
        self.lithology = lithology


class Timeseries:
    def __init__(self, data: pd.DataFrame):
        self.data = data
        # self.remove_outliers()

    def __getitem__(self, item):
        return self.data[item]

    def __setitem__(self, key, values):
        self.data[key] = values

    def remove_outliers(self):
        for col in self.data.columns:
            self[col] = remove_outliers(self[col])

    def select_daterange(self, start_date, end_date):
        """Selects data within a specified date range."""
        sel = self.data.loc[start_date:end_date]
        return self.__class__(sel)

    def reindex_time(self, start_date, end_date, freq="h"):
        """Reindexes the data to a specified time frequency."""
        date_range = pd.date_range(
            start=pd.to_datetime(start_date, format="%Y-%m-%d"),
            end=pd.to_datetime(end_date, format="%Y-%m-%d"),
            freq=freq,
        )

        reindexed = self.data.reindex(date_range, method="nearest", limit=1)
        return self.__class__(reindexed)

    def resample(self, freq="D"):
        resampled = self.data.resample(freq).mean()
        return self.__class__(resampled)
