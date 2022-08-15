import pandas as pd


def print_dim(df):
    rows, columns = df.shape
    print(f'This DataFrame contains {rows} rows and {columns} columns')