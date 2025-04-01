import pandas as pd

from DiverDataProcessor.base import HandReading, ObservationWell, Timeseries


def _water_column_from(
    baro: pd.Series, diver: pd.Series, water_density: float = 1000.0
) -> Timeseries:
    """
    Calculate the height of the water column above the diver by subtracting air pressure
    from diver pressure and converting pressure to water height, based on density of fresh water.

    Parameters
    ----------
    baro : Timeseries
        The atmospheric air pressure (mH2O).
    diver : Timeseries
        The pressure recorded by the diver (mH2O).
    water_density : float, optional
        The density of water in kg/m3. Default is 1000.0 kg/m3.

    Returns
    -------
    Timeseries
        The height of the water column above the diver in meters (m), as a Timeseries.

    """

    gravitational_acceleration = 9.80665  # m/s2

    water_pressure = diver["diver_pressure (mH2O)"] - baro["air_pressure (mH2O)"]
    water_column = (9806.65 * water_pressure) / (
        water_density * gravitational_acceleration
    )

    return Timeseries(water_column.to_frame("water_column (m)"))


def _water_column_at_datetime(
    water_column: Timeseries, datetime: pd.Timestamp
) -> float:
    """
    Find the closest diver reading to a specified date and time.

    Parameters
    ----------
    water_column : Timeseries
        The DataFrame containing water column timeseries.
    datetime : pd.Timestamp
        The target datetime to find the closest reading.

    Returns
    -------
    float
        The row of the DataFrame closest to the specified datetime.

    """
    closest_index = water_column.data.index.get_indexer([datetime], method="nearest")[0]
    return water_column["water_column (m)"].iloc[closest_index]


def _diver_position_to_datum(water_column_above_diver, handreading, top_well):
    """
    Calculate the diver's position relative to the datum (e.g., ground level).

    Parameters
    ----------
    handreading : float
        The manual reading taken from the well.
    water_column : float
        The height of the water column at datetime of handreading.
    top_well : float
        The height of the surface above the datum.
    diver_position_to_surface : float
        The diver's position relative to the water surface.

    Returns
    -------
    float
        Diver's position relative to the datum in meters.

    """
    cable_length = water_column_above_diver + handreading
    return top_well - cable_length


def baro_compensate(
    baro: Timeseries,
    diver: Timeseries,
    handreading: HandReading,
    observation_well: ObservationWell,
    method: str = "cable",
):
    """
    Compensates diver pressure data using barometric pressure data and calculates
    water level relative to a datum.

    Parameters
    ----------
    baro :  Timeseries
        A timeseries of barometric pressure data.
    diver :  Timeseries
        A timeseries of diver pressure data.
    handreading :  HandReading
        A handreading object containing manual water level readings and their timestamps.
    observation_well :  ObservationWell
        An observation well object containing metadata such as the top of the well
        and the diver's position relative to the datum.
    method : str, optional
        The method to use for compensation. Options are:
        - "handreading": Uses manual handreading data to calculate the diver's position
          relative to the datum.
        - "cable": Uses the pre-defined diver-to-datum distance from the observation well.
        Default is "cable".
    Returns
    -------
    Timeseries
        A timeseries of water levels relative to the datum, with the column labeled
        as "water_level (m datum)".
    Raises
    ------
    ValueError
        If the specified method is not "handreading" or "cable".

    """
    water_column = _water_column_from(baro, diver)

    if method == "handreading":
        water_column_at_handreading = _water_column_at_datetime(
            water_column, handreading.datetime
        )
        diver_to_datum = _diver_position_to_datum(
            water_column_at_handreading, handreading.reading, observation_well.top_well
        )
    elif method == "cable":
        diver_to_datum = observation_well.diver_to_datum
    else:
        raise ValueError('Method not valid, use: "handreading", or "cable".')

    water_level = diver_to_datum + water_column["water_column (m)"]

    return Timeseries(water_level.to_frame("water_level (m datum)"))
