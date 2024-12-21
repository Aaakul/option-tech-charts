import os
import pandas as pd
from datetime import datetime
from helper import load_csv, save_to_csv, get_current_date_string

def filter_data(df):
    """
    Filter the DataFrame based on specified criteria.

    :param df: The input DataFrame.
    :return: A filtered DataFrame.
    """
    # Calculate the median of strike prices
    strike_mean = df['strike'].median()

    # Filter strikes greater than or equal to the median
    filtered_df = df[df['strike'] >= strike_mean]

    # Calculate the mean of put and call open interest
    put_open_interest_lower_bound = filtered_df['put_open_interest'].mean()
    call_open_interest_lower_bound = filtered_df['call_open_interest'].mean()

    # Filter rows where put or call open interest is greater than its respective lower bound
    second_filtered_df = filtered_df[
        (filtered_df['put_open_interest'] > put_open_interest_lower_bound) |
        (filtered_df['call_open_interest'] > call_open_interest_lower_bound)
    ]
    
    return second_filtered_df

def main(symbol):
    """
    Main function to execute the data filtering process.

    :param symbol: The stock or option symbol to process.
    """
    # Define file paths
    date_str = get_current_date_string()
    input_file_name = f'{symbol}_summary_{date_str}.csv'
    input_dir = f'./data/{symbol}'
    input_path = os.path.join(input_dir, input_file_name)

    # Load the CSV file into a DataFrame
    df = load_csv(input_path)
    if df is None:
        print("Failed to load the CSV file. Exiting.")
        return

    # Filter the data
    filtered_df = filter_data(df)

    # Define the output file name with year and month
    output_file_name = f'{symbol}_filtered_{date_str}.csv'
    output_path = os.path.join(input_dir, output_file_name)

    # Save the filtered data to a new CSV file
    save_to_csv(filtered_df, output_path)

if __name__ == "__main__":
    # Specify the symbol to process
    symbol = 'SPY'
    main(symbol)