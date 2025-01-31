from dotenv import load_dotenv
import pandas as pd
from datetime import datetime, timedelta
import os
from helper import load_csv, create_output_directory, save_to_csv, get_current_date_string

def get_today_and_end_of_month():
    """
    Get today's date and the last day of the current month.

    :return: A tuple containing today's date and the last day of the month as strings in 'YYYY-MM-DD' format.
    """
    today = datetime.now()
    if today.month == 12:
        next_month = today.replace(year=today.year + 1, month=1, day=1)
    else:
        next_month = today.replace(month=today.month + 1, day=1)
    last_day_of_month = next_month - timedelta(days=1)
    return today.strftime('%Y-%m-%d'), last_day_of_month.strftime('%Y-%m-%d')

def filter_data(df, today, last_day):
    """
    Filter the DataFrame for data from today to the end of the current month based on expiration date and other criteria.

    :param df: The input DataFrame.
    :param today: Today's date as a string in 'YYYY-MM-DD' format.
    :param last_day: The last day of the current month as a string in 'YYYY-MM-DD' format.
    :return: A filtered DataFrame.
    """
    df['expiration'] = pd.to_datetime(df['expiration'])
    filtered_df = df[(df['expiration'] >= today) & 
                     (df['expiration'] <= last_day) & 
                     (df['delta'].abs() > 0.05) & 
                     (df['open_interest'] > 0)]
    filtered_columns = ['expiration', 'strike', 'type', 'open_interest', 'implied_volatility', 'delta', 'gamma']
    return filtered_df[filtered_columns]

def main(symbol):
    today, last_day = get_today_and_end_of_month()
    input_path = f'./data/{symbol}/historical_options_{symbol}.csv'
    df = load_csv(input_path)
    if df is None:
        print("Failed to load the CSV file. Exiting.")
        return False
    filtered_df = filter_data(df, today, last_day)
    create_output_directory(f"./data/{symbol}")
    output_path = os.path.join(f"./data/{symbol}", f'{symbol}_{get_current_date_string()}.csv')
    return save_to_csv(filtered_df, output_path)

load_dotenv(dotenv_path='.env.public')
symbols = os.getenv('SYMBOLS', '').split(',')

if __name__ == '__main__':
    if not symbols or symbols == ['']:
        print("No symbols provided in the .env.public file under SYMBOLS.")
    else:
        for symbol in symbols:
            success = main(symbol.strip())
            if not success:
                print(f"Failed to process CSV file for symbol {symbol}.")