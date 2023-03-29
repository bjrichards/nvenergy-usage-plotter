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


def create_plot(file_name: str):
    # Grab file path
    INPUT_FILE_PATH: str = cf.App_Config.input_file_path + file_name
    OUTPUT_FILE_PATH: str = cf.App_Config.output_file_path + file_name.split('.')[0]

    # Import the data
    df: pd.DataFrame = pd.read_csv(INPUT_FILE_PATH)

    # Include only required data
    plot_df: pd.DataFrame = df.pivot_table(
        "Usage", "Startdate", "powerFlow", aggfunc="sum"
    )

    # Create bar chart
    usage_plot: plt.Axes = plot_df.plot.bar(stacked=False, rot=45)

    # Add labels on top of each bar showing the y-axis value (usage)
    for container in usage_plot.containers:  # type:ignore
        usage_plot.bar_label(container)

    # Save new df to file
    if not os.path.exists(OUTPUT_FILE_PATH):
        os.mkdir(OUTPUT_FILE_PATH)
    plot_df.to_csv(os.path.join(OUTPUT_FILE_PATH, file_name))

    # Bar chart configurations
    plt.title("Power Usage")
    plt.xlabel("Date")
    plt.ylabel("Usage (kWh)")
    plt.tight_layout()
    plt.legend(title="Power Flow")
    
    # Save figure to output folder
    plt.savefig(os.path.join(OUTPUT_FILE_PATH, file_name.split(".")[0]))

    # Show figure
    plt.show()


if __name__ == "__main__":
    import sys

    file_name: str
    if len(sys.argv) > 1:
        for i in range(1, len(sys.argv)):
            file_name = sys.argv[i]
            create_plot(file_name)
    else:
        file_name = cf.User_Config.file_name
        create_plot(file_name)
