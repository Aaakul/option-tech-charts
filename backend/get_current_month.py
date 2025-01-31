from dotenv import load_dotenv
import pandas as pd
from datetime import datetime, timedelta
import os
from helper import load_csv, create_output_directory, save_to_csv, get_current_date_string

def get_today_and_end_of_month():
    today = datetime.now()
    if today.month == 12:
        next_month = today.replace(year=today.year + 1, month=1, day=1)
    else:
        next_month = today.replace(month=today.month + 1, day=1)
    last_day_of_month = next_month - timedelta(days=1)
    return today.strftime('%Y-%m-%d'), last_day_of_month.strftime('%Y-%m-%d')

def filter_data(df, today, last_day):
    df['expiration'] = pd.to_datetime(df['expiration'])
    filtered_df = df[(df['expiration'] >= today) & 
                     (df['expiration'] <= last_day) & 
                     (df['delta'].abs() > 0.05) & 
                     (df['open_interest'] > 0)]
    filtered_columns = ['expiration', 'strike', 'type', 'open_interest', 'implied_volatility', 'delta', 'gamma']
    return filtered_df[filtered_columns]

def filter_next_expiration(filtered_df):
    if filtered_df.empty:
        return pd.DataFrame()
    next_expiration = filtered_df.iloc[0]['expiration']
    next_expiration_df = filtered_df[filtered_df['expiration'] == next_expiration]
    return next_expiration_df

def main(symbol):
    today, last_day = get_today_and_end_of_month()
    input_path = f'./data/{symbol}/historical_options_{symbol}.csv'
    df = load_csv(input_path)
    if df is None:
        return False
    filtered_df = filter_data(df, today, last_day)
    
    if filtered_df.empty:
        print(f"No data available for {today} for symbol {symbol}.")
        return True
    
    create_output_directory(f"./data/{symbol}")
    output_path = os.path.join(f"./data/{symbol}", f'{symbol}_{get_current_date_string()}.csv')
    if not save_to_csv(filtered_df, output_path):
        return False

    # Generate next expiration date file
    next_expiration_df = filter_next_expiration(filtered_df)
    if not next_expiration_df.empty:
        next_output_path = os.path.join(f"./data/{symbol}", f'{symbol}_0dte.csv')
        return save_to_csv(next_expiration_df, next_output_path)
    else:
        print(f"No specific next expiration date data found for symbol {symbol}.")
        return True

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