import numpy as np
import pandas as pd
import pytest
from numpy.testing import (
    assert_approx_equal,
    assert_array_almost_equal,
    assert_array_equal,
)

from DiverDataProcessor import processing, readers


class TestCompensation:
    @pytest.mark.unittest
    def test_water_column_from(self, simple_diverdata, simple_barodata):

        water_column = processing._water_column_from(simple_barodata, simple_diverdata)
        expected_results = np.array([0.0, 10.0, 20.0, 30.0, 30.0])
        assert isinstance(water_column, readers.Timeseries)
        assert water_column.data.shape[0] == simple_diverdata.data.shape[0]
        assert water_column.data.columns.tolist() == ["water_column (m)"]
        assert_array_equal(water_column["water_column (m)"].values, expected_results)

    @pytest.mark.unittest
    def test_water_column_at_datetime(self, simple_barodata, simple_diverdata):
        water_column = processing._water_column_from(simple_barodata, simple_diverdata)
        datetime = pd.Timestamp("2023-01-01 00:02:29")
        expected_value = 20.0
        result = processing._water_column_at_datetime(water_column, datetime)
        assert isinstance(result, float)
        assert result == expected_value

    @pytest.mark.unittest
    def test_diver_position_to_datum(self):
        water_column_at_datetime = 0.5
        handreading = 0.25
        top_well = 0.0

        results = processing._diver_position_to_datum(
            water_column_at_datetime, handreading, top_well
        )
        exected_results = -0.75
        assert isinstance(results, float)
        assert results == exected_results

    def test_baro_compensate(self, simple_diverdata):
        diver_data = readers.read_td_diver(simple_diverdata)
        baro_data = readers.read_baro_diver(simple_diverdata)

        compensated_data = processing.baro_compensate(diver_data, baro_data)

        assert isinstance(compensated_data, pd.DataFrame)
        assert compensated_data.shape == diver_data.data.shape
        assert set(compensated_data.columns) == set(diver_data.data.columns)

        # Check if the compensation is applied correctly
        assert np.all(np.isfinite(compensated_data.values))
