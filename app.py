# Desc: Reads in a data dump of usage from NV Energy and plots the recieved and
#   delivered data per day as a bar chart. Outputs the filtered down data as new csv.
#
# Written by Braeden Richards
# Created on March 27, 2023
# Contact: braedae.software@gmail.com
#
# Last updated on March 27, 2023
# Last updated by Braeden Richards

import pandas as pd
import matplotlib.pyplot as plt
import config as cf
import os


def work_data(file_name: str) -> None:
    """Pulls in data from filename, filters data and plots to bar chart."""
    # Grab file path
    INPUT_FILE_PATH: str = cf.App_Config.input_file_path + file_name
    OUTPUT_FILE_PATH: str = cf.App_Config.output_file_path + file_name.split(".")[0]
    OUTPUT_PLOT_PATH: str = os.path.join(OUTPUT_FILE_PATH, file_name.split(".")[0])

    # Import the data
    df: pd.DataFrame = pd.read_csv(INPUT_FILE_PATH)

    # Filter to only needed data
    plot_df = get_data(df=df)

    # Save new df to file
    if not os.path.exists(path=OUTPUT_FILE_PATH):
        os.mkdir(path=OUTPUT_FILE_PATH)
    plot_df.to_csv(os.path.join(OUTPUT_FILE_PATH, file_name))

    # Create plot, show to user and save it to file
    create_plot(df=plot_df, output_file=OUTPUT_PLOT_PATH)


def get_data(df: pd.DataFrame) -> pd.DataFrame:
    """Grabs only required data from input dataframe."""
    # Include only required data
    plot_df: pd.DataFrame = df.pivot_table(
        values="Usage", index="Startdate", columns="powerFlow", aggfunc="sum"
    )
    return plot_df


def create_plot(df: pd.DataFrame, output_file: str) -> None:
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
    plt.xlabel(xlabel="Date")
    plt.ylabel(ylabel="Usage (kWh)")
    plt.tight_layout()
    plt.legend(title="Power Flow")

    # Save figure to output folder
    plt.savefig(output_file)

    # Show figure
    plt.show()


if __name__ == "__main__":
    import sys

    file_name: str
    if len(sys.argv) > 1:
        for i in range(1, len(sys.argv)):
            file_name = sys.argv[i]
            work_data(file_name=file_name)
    else:
        file_name = cf.User_Config.file_name
        work_data(file_name=file_name)
