"""Pytest configuration file"""
import pathlib
import pandas as pd
import pytest

from life_expectancy.cleaning import load_data
from . import FIXTURES_DIR, OUTPUT_DIR

@pytest.fixture(autouse=True)
def run_before_and_after_tests() -> None:
    """Fixture to execute commands befor and after a test is run"""
    # Setup: fill with any logic you want

    yield # this is where the testing happens

    # Teardown : fill with any logic you want
    file_path = OUTPUT_DIR / "pt_life_expectancy.csv"
    file_path.unlink(missing_ok=True)


@pytest.fixture(scope="session")
def pt_life_expectancy_expected() -> pd.DataFrame:
    """Fixture to load the expected output of the cleaning script."""

    expected_df = pd.read_csv(
        FIXTURES_DIR / "pt_life_expectancy_expected.csv")

    expected_df = (
        expected_df.
        fillna(0).
        astype({"year":int, "value": float})
    )

    return expected_df

@pytest.fixture(scope="session")
def pt_life_expectancy_input() -> pd.DataFrame:
    """Fixture to load and clean the original dataframe
    and only keep the first 5 rows."""

    created_df = load_data()
    return created_df


@pytest.fixture(scope="session")
def monkeypatch() -> pytest.MonkeyPatch:
    """Instantiating MonkeyPatch object."""

    patch = pytest.MonkeyPatch()

    return patch

@pytest.fixture(scope="session")
def eu_life_expectancy_raw() -> pd.DataFrame:
    """Fixture to load the expected output of the cleaning script"""
    baseline_df = pd.read_csv(
        FIXTURES_DIR / "eu_life_expectancy_raw.tsv")

    return  baseline_df
