import numpy as np
import pandas as pd
import pytest
from numpy.testing import (
    assert_approx_equal,
    assert_array_almost_equal,
    assert_array_equal,
)

from DiverDataProcessor import readers


@pytest.mark.unittest
def test_read_td_diver(simple_diverdata):
    diver_data = readers.read_td_diver(simple_diverdata)

    expected_columns = [
        "temperature (degC)",
        "diver_pressure (mH2O)",
    ]

    assert diver_data.data.shape == (72, 2)
    assert diver_data.data.columns.tolist() == expected_columns
    assert isinstance(diver_data.data.index, pd.DatetimeIndex)
