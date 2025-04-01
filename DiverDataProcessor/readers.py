import numpy as np
import pandas as pd

from DiverDataProcessor.base import Timeseries


def read_td_diver(filepath) -> Timeseries:
    diver_data = pd.read_csv(
        filepath,
        usecols=[0, 1, 2],
        names=["date", "diver_pressure (cmH2O)", "temperature (degC)"],
        decimal=",",
        skiprows=52,
        delimiter=";",
        encoding="ISO-8859-1",
        engine="python",
    )
    diver_data = diver_data[:-1].replace("     ", np.nan)
    diver_data["diver_pressure (mH2O)"] = (
        pd.to_numeric(diver_data["diver_pressure (cmH2O)"]) / 100
    )
    diver_data = diver_data.drop(columns=["diver_pressure (cmH2O)"])
    diver_data["temperature (degC)"] = pd.to_numeric(diver_data["temperature (degC)"])
    diver_data["date"] = pd.to_datetime(diver_data["date"], format="%Y/%m/%d %H:%M:%S")
    diver_data = diver_data.set_index("date")
    return Timeseries(diver_data)


def read_ec_diver(filepath) -> Timeseries:
    diver_data = pd.read_csv(
        filepath,
        usecols=[0, 1, 2, 3],
        names=[
            "date",
            "diver_pressure (cmH2O)",
            "temperature (degC)",
            "electrical_conductivity (mS/cm)",
        ],
        decimal=",",
        skiprows=64,
        delimiter=";",
        encoding="ISO-8859-1",
        engine="python",
    )
    diver_data = diver_data[:-1].replace("     ", np.nan)
    diver_data["diver_pressure (mH2O)"] = (
        pd.to_numeric(diver_data["diver_pressure (cmH2O)"]) / 100
    )
    diver_data = diver_data.drop(columns=["diver_pressure (cmH2O)"])
    diver_data["electrical_conductivity (mS/cm)"] = pd.to_numeric(
        diver_data["electrical_conductivity (mS/cm)"]
    )
    diver_data["temperature (degC)"] = pd.to_numeric(diver_data["temperature (degC)"])
    diver_data["date"] = pd.to_datetime(diver_data["date"], format="%Y/%m/%d %H:%M:%S")
    diver_data = diver_data.set_index("date")
    return Timeseries(diver_data)


def read_baro_diver(filepath) -> Timeseries:
    diver_data = pd.read_csv(
        filepath,
        usecols=[0, 1, 2],
        names=["date", "air_pressure (cmH2O)", "temperature (degC)"],
        decimal=",",
        skiprows=52,
        delimiter=";",
        encoding="ISO-8859-1",
        engine="python",
    )
    diver_data = diver_data[:-1].replace("     ", np.nan)
    diver_data["air_pressure (mH2O)"] = (
        pd.to_numeric(diver_data["air_pressure (cmH2O)"]) / 100
    )
    diver_data = diver_data.drop(columns=["air_pressure (cmH2O)"])
    diver_data["temperature (degC)"] = pd.to_numeric(diver_data["temperature (degC)"])
    diver_data["date"] = pd.to_datetime(diver_data["date"], format="%Y/%m/%d %H:%M:%S")
    diver_data = diver_data.set_index("date")
    return Timeseries(diver_data)


def read_diver_link(filepath) -> Timeseries:
    diver_data = pd.read_csv(
        filepath,
        parse_dates=["Date and time (UTC-06:00)"],
        usecols=[0, 2, 3],
    )
    diver_data.columns = ["date", "temperature (degC)", "diver_pressure (cmH2O)"]
    diver_data["diver_pressure (mH2O)"] = (
        pd.to_numeric(diver_data["diver_pressure (cmH2O)"]) / 100
    )
    diver_data = diver_data.drop(columns=["diver_pressure (cmH2O)"])
    diver_data["temperature (degC)"] = pd.to_numeric(diver_data["temperature (degC)"])
    diver_data["date"] = pd.to_datetime(diver_data["date"], format="%d/%m/%Y %H:%M:%S")
    diver_data = diver_data.set_index("date")
    return Timeseries(diver_data)


def read_precipitation(path) -> Timeseries:
    precipitation = pd.read_csv(path, delimiter=";", decimal=",")
    precipitation.columns = ["date", "precipitation (mm)"]
    precipitation["date"] = pd.to_datetime(precipitation["date"], format="%d-%m-%Y")
    precipitation = precipitation.set_index("date")
    return Timeseries(precipitation)
