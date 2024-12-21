import pandas as pd
from datetime import datetime, timedelta
import os
from helper import load_csv, create_output_directory, save_to_csv, get_current_date_string

def get_month_dates():
    """
    Get the first and last dates of the current month.

    :return: A tuple containing the first and last day of the month as strings in 'YYYY-MM-DD' format.
    """
    today = datetime.now()
    first_day_of_month = today.replace(day=1)
    if today.month == 12:
        next_month = today.replace(year=today.year + 1, month=1, day=1)
    else:
        next_month = today.replace(month=today.month + 1, day=1)
    last_day_of_month = next_month - timedelta(days=1)
    return first_day_of_month.strftime('%Y-%m-%d'), last_day_of_month.strftime('%Y-%m-%d')

def filter_data(df, first_day, last_day):
    """
    Filter the DataFrame for the current month's data based on expiration date and other criteria.

    :param df: The input DataFrame.
    :param first_day: The first day of the current month as a string in 'YYYY-MM-DD' format.
    :param last_day: The last day of the current month as a string in 'YYYY-MM-DD' format.
    :return: A filtered DataFrame.
    """
    # Convert 'expiration' column to datetime
    df['expiration'] = pd.to_datetime(df['expiration'])

    # Apply filtering conditions
    filtered_df = df[(df['expiration'] >= first_day) & 
                     (df['expiration'] <= last_day) & 
                     (df['delta'].abs() > 0.05) & 
                     (df['open_interest'] > 0)]

    # Select only required columns
    filtered_columns = ['expiration', 'strike', 'type', 'open_interest', 'implied_volatility', 'delta', 'gamma']
    return filtered_df[filtered_columns]

def main(symbol):
    """
    Main function to execute the data filtering process.

    :param symbol: The stock or option symbol to process.
    """
    # Define file paths
    input_dir = f'./data/{symbol}'
    input_file_name = f'historical_options_{symbol}.csv'
    input_path = os.path.join(input_dir, input_file_name)

    # Get the first and last dates of the current month
    first_day, last_day = get_month_dates()

    # Load the CSV file into a DataFrame
    df = load_csv(input_path)
    if df is None:
        print("Failed to load the CSV file. Exiting.")
        return

    # Filter the data
    filtered_df = filter_data(df, first_day, last_day)

    # Create output directory if it doesn't exist
    create_output_directory(input_dir)

    # Define the output file name with year and month
    date_str = get_current_date_string()
    output_file_name = f'{symbol}_{date_str}.csv'
    output_path = os.path.join(input_dir, output_file_name)

    # Save the filtered data to a new CSV file
    save_to_csv(filtered_df, output_path)

if __name__ == "__main__":
    # Specify the symbol to process
    symbol = 'SPY'
    main(symbol)