"""Tests for the cleaning module"""
import pandas as pd
import pytest
from life_expectancy.cleaning import clean_data, save_data, main

from . import OUTPUT_DIR

def test_end_to_end(pt_life_expectancy_expected):
    """Run the `clean_data` function and compare the output to the expected output"""
    main()
    pt_life_expectancy_actual = pd.read_csv(
        OUTPUT_DIR / "pt_life_expectancy.csv"
    ).head(50)

    pt_life_expectancy_expected = pt_life_expectancy_expected.head(50)

    pd.testing.assert_frame_equal(
        pt_life_expectancy_actual, pt_life_expectancy_expected
    )


def test_clean_data_csv(
    pt_life_expectancy_input_csv : pd.DataFrame,
    pt_life_expectancy_expected : pd.DataFrame) -> None :
    """Use clean_data function.
    Assert top 5 lines of created and expected dataframes."""

    pt_life_expectancy_input_csv = clean_data(pt_life_expectancy_input_csv,'csv')
    pt_life_expectancy_input_csv = pt_life_expectancy_input_csv.reset_index(drop=True).iloc[:5]
    pt_life_expectancy_expected = pt_life_expectancy_expected.iloc[:5]

    pd.testing.assert_frame_equal(
        pt_life_expectancy_input_csv,
        pt_life_expectancy_expected
    )

def test_clean_data_json(
    pt_life_expectancy_input_json : pd.DataFrame,
    pt_life_expectancy_expected : pd.DataFrame) -> None :
    """Use clean_data function.
    Assert top 5 lines of created and expected dataframes."""

    pt_life_expectancy_input_json = clean_data(pt_life_expectancy_input_json,'json')
    pt_life_expectancy_input_json = pt_life_expectancy_input_json.reset_index(drop=True).iloc[:5]
    pt_life_expectancy_expected = pt_life_expectancy_expected.iloc[:5]

    pd.testing.assert_frame_equal(
        pt_life_expectancy_input_json,
        pt_life_expectancy_expected
    )


def test_save_data(
    monkeypatch : pytest.MonkeyPatch,
    pt_life_expectancy_expected : pd.DataFrame) -> None :
    """Patch to_csv method, testing save_data function."""

    def _mockreturn_save(*args, **kwargs) -> str :
        """Result to receive when mock."""
        # pylint: disable=unused-argument

        return "DataFrame Saved."

    monkeypatch.setattr(pt_life_expectancy_expected, "to_csv",  _mockreturn_save)

    assert save_data(pt_life_expectancy_expected) == "DataFrame Saved."
