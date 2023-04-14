class User_Config:
    file_name: str = "input.csv"
    date_grouping: str = "D"  # Options are: D -> Date, M -> Month, Y -> Year
    label_decimal_num: int = 1  # How many decimal points


class App_Config:
    input_file_path: str = "./input/"
    output_file_path: str = "./output/"
