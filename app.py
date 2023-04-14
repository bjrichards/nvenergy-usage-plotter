# Desc: Reads in a data dump of usage from NV Energy and plots the recieved and
#   delivered data as a bar chart according to period grouping value
#   (date, month, etc.). Outputs the filtered down data as new csv.
#
# Written by Braeden Richards
# Created on March 27, 2023
# Contact: braedae.software@gmail.com
#
# Last updated on April 13, 2023

import pandas as pd
import matplotlib.pyplot as plt

import enum
import os

import config as cf


class Date_Levels(enum.Enum):
    """Enum containing data grouping levels."""

    DAY = "Day"
    MONTH = "Month"
    YEAR = "Year"


def work_data(file_name: str, date_level: Date_Levels = Date_Levels.DAY) -> None:
    """Pulls in data from filename, filters data and plots to bar chart."""
    # Grab file path
    INPUT_FILE_PATH: str = cf.App_Config.input_file_path + file_name
    OUTPUT_FILE_PATH: str = cf.App_Config.output_file_path + file_name.split(".")[0]
    OUTPUT_PLOT_PATH: str = os.path.join(OUTPUT_FILE_PATH, file_name.split(".")[0])

    # Import the data
    df: pd.DataFrame = pd.read_csv(INPUT_FILE_PATH)

    # Filter to only needed data
    plot_df = get_data(df=df, date_level=date_level)

    # Save new df to file
    if not os.path.exists(path=OUTPUT_FILE_PATH):
        os.mkdir(path=OUTPUT_FILE_PATH)
    plot_df.to_csv(os.path.join(OUTPUT_FILE_PATH, file_name))

    # Create plot, show to user and save it to file
    create_plot(df=plot_df, output_file=OUTPUT_PLOT_PATH, xlabel=date_level.value)


def get_data(
    df: pd.DataFrame, date_level: Date_Levels = Date_Levels.DAY
) -> pd.DataFrame:
    """Returns only required data from input dataframe. Groups data based on date_level parameter."""
    # Include only required data
    plot_df: pd.DataFrame = df.pivot_table(
        values="Usage", index="Startdate", columns="powerFlow", aggfunc="sum"
    )

    # Change the Startdate index into a DateTimeIndex for grouping purposes
    plot_df.index = pd.to_datetime(plot_df.index)

    # If grouped by year, group the DateTimeIndex Startdate by year and then convert to Year PeriodIndex for readability.
    if date_level == Date_Levels.YEAR:
        plot_df = plot_df.groupby(pd.Grouper(freq="Y", level="Startdate")).sum()
        plot_df.index = pd.to_datetime(plot_df.index).to_period("Y")

    # If grouped by month, group the DateTimeIndex Startdate by month and then convert to Month PeriodIndex for readability.
    elif date_level == Date_Levels.MONTH:
        plot_df = plot_df.groupby(pd.Grouper(freq="M", level="Startdate")).sum()
        plot_df.index = pd.to_datetime(plot_df.index).to_period("M")

    # If grouped by day, convert the DateTimeIndex to PeriodIndex for readability.
    elif date_level == Date_Levels.DAY:
        plot_df.index = plot_df.index.to_period("D")

    return plot_df


def create_plot(df: pd.DataFrame, output_file: str, xlabel: str = "Date") -> None:
    """Creates bar chart based on dataframe. Shows to user and outputs to output_file."""
    # Create bar chart
    usage_plot: plt.Axes = df.plot.bar(stacked=False, rot=45)

    # Add labels on top of each bar showing the y-axis value (usage)
    for container in usage_plot.containers:  # type:ignore
        usage_plot.bar_label(
            container=container, fmt=f"%.{cf.User_Config.label_decimal_num}f"
        )

    # Bar chart configurations
    plt.title(label="Power Usage")
    plt.xlabel(xlabel=xlabel)
    plt.ylabel(ylabel="Usage (kWh)")
    plt.tight_layout()
    plt.legend(title="Power Flow")

    # Save figure to output folder
    plt.savefig(output_file)

    # Show figure
    plt.show()


def get_date_grouping(key: str = "D") -> Date_Levels:
    """Returns the date level enum from the date grouping key value passed in."""
    result: Date_Levels
    if key == "D":
        result = Date_Levels.DAY
    elif key == "M":
        result = Date_Levels.MONTH
    else:
        result = Date_Levels.DAY
    return result


if __name__ == "__main__":
    import sys

    file_name: str
    # If including command line arguments or running against multiple files
    if len(sys.argv) > 1:
        # Run at month grouping level
        if sys.argv[1] == "-m":
            for i in range(2, len(sys.argv)):
                file_name = sys.argv[i]
                work_data(file_name=file_name, date_level=Date_Levels.MONTH)
        elif sys.argv[1] == "-y":
            for i in range(2, len(sys.argv)):
                file_name = sys.argv[i]
                work_data(file_name=file_name, date_level=Date_Levels.YEAR)
        elif sys.argv[1] == "-d":
            for i in range(2, len(sys.argv)):
                file_name = sys.argv[i]
                work_data(file_name=file_name, date_level=Date_Levels.DAY)
        # Run at day grouping level
        else:
            for i in range(1, len(sys.argv)):
                file_name = sys.argv[i]
                work_data(file_name=file_name, date_level=Date_Levels.DAY)

    # If running based on config file variables
    else:
        file_name = cf.User_Config.file_name
        date_grouping = get_date_grouping(cf.User_Config.date_grouping)
        work_data(file_name=file_name, date_level=date_grouping)
