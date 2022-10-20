"""Cleaning Life Expectancy Data for Assignment 1- Data Cleaning Challenge."""

#import pathlib
import argparse
import pandas as pd
import numpy as np


#DATA_PATH =  pathlib.Path().resolve().parents[0] / 'life_expectancy/data'

def clean_data(region= None):
    """ Clean_data function does the following:
        -Loads file.
        -Melts Date columns into a single column;
        -Split first column into 4 different;
        -Remove NaN's;
        -Transform columns value and year and its datatypes
        -Filter region column, only for Portugal (PT).
        -Save output into csv file, without index.
    """

    life_expectancy = pd.read_csv(
        r"C:\Users\crocs\OneDrive - Universidade de Lisboa\Ambiente de Trabalho" \
            r"\Data Science Courses\faast_se_foundations\faast-foundations" \
                r"\assignments\life_expectancy\data\eu_life_expectancy_raw.tsv",
                sep="\t")

    life_expectancy.columns =  [
        column_title.replace("\\","") for column_title 
        in life_expectancy.columns
        ]

    life_expectancy = pd.melt(life_expectancy,
                            id_vars= life_expectancy.columns[0],
                            var_name= "year",
                            value_vars= life_expectancy.columns[1:],
                            value_name= "value")

    life_expectancy[["unit","sex","age","region"]] = (
        life_expectancy["unit,sex,age,geotime"].
        str.split(',', expand=True)
        )

    life_expectancy = (
        life_expectancy.
        drop(columns="unit,sex,age,geotime").
        replace(": ",np.NaN).
        dropna(how="any")
        )


    life_expectancy["value"] = (
        life_expectancy["value"].
        str.split().str[0]
    )

    if region is None:
        life_expectancy = life_expectancy[life_expectancy["region"]== "PT"]
    else:
        life_expectancy = life_expectancy[life_expectancy["region"]== region]

    life_expectancy = life_expectancy.astype(
        {"year":int, "value": float})

    life_expectancy = life_expectancy[
        ["unit","sex","age","region","year","value"]
        ]
    life_expectancy.to_csv(
        r"C:\Users\crocs\OneDrive - Universidade de Lisboa\Ambiente de Trabalho" \
            r"\Data Science Courses\faast_se_foundations\faast-foundations" \
                r"\assignments\life_expectancy\data\pt_life_expectancy.csv",
                index= False)


if __name__ == "__main__": # pragma: no cover

    parser = argparse.ArgumentParser(description='Clean data based on specific Region.')
    parser.add_argument(
        '-r',
        '--region',
        nargs="?",
        type=str,
        help="Indicate preferred country with 2 capital letters (default= 'PT').",
        const="PT",
        required=True
    )
    args = parser.parse_args()

    region_letters = args.region

    clean_data(region_letters)
