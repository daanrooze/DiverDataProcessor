from pathlib import Path

import geopandas as gpd
import pandas as pd
import pytest

from DiverDataProcessor import base


@pytest.fixture
def simple_tddata():
    """
    Small extraction of 4 soilunits from the BRO soilmap geopackage for testing purposes.

    """
    return Path(__file__).parent / r"data/test_tddiver.csv"


@pytest.fixture
def simple_diverdata():
    data = {
        "date": [
            "2023-01-01 00:00:00",
            "2023-01-01 00:01:00",
            "2023-01-01 00:02:00",
            "2023-01-01 00:03:00",
            "2023-01-01 00:04:00",
        ],
        "diver_pressure (mH2O)": [1000, 1010, 1020, 1030, 1040],
        "temperature (degC)": [10, 11, 12, 13, 14],
    }
    df = pd.DataFrame(data)
    df["date"] = pd.to_datetime(df["date"], format="%Y-%m-%d %H:%M:%S")
    return base.Timeseries(df.set_index("date"))


@pytest.fixture
def simple_barodata():
    data = {
        "date": [
            "2023-01-01 00:00:00",
            "2023-01-01 00:01:00",
            "2023-01-01 00:02:00",
            "2023-01-01 00:03:00",
            "2023-01-01 00:04:00",
        ],
        "air_pressure (mH2O)": [1000, 1000, 1000, 1000, 1010],
        "temperature (degC)": [10, 11, 12, 13, 14],
    }
    df = pd.DataFrame(data)
    df["date"] = pd.to_datetime(df["date"], format="%Y-%m-%d %H:%M:%S")
    return base.Timeseries(df.set_index("date"))
