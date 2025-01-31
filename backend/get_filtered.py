import os

from dotenv import load_dotenv
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

def process_csv(symbol, file_suffix):
    """
    Main function to execute the data filtering process.

    :param symbol: The stock or option symbol to process.
    :return: True if the process was successful, False otherwise.
    """
    # Define file paths
    input_file_name = f'{symbol}_summary{file_suffix}.csv'
    input_dir = f'./data/{symbol}'
    input_path = os.path.join(input_dir, input_file_name)


    # Define the output file name with year and month
    output_file_name = f'{symbol}_filtered{file_suffix}.csv'
    output_path = os.path.join(input_dir, output_file_name)

    # Load the CSV file into a DataFrame
    df = load_csv(input_path)
    if df is None:
        return False

    # Filter the data
    filtered_df = filter_data(df)

    # Save the filtered data to a new CSV file
    return save_to_csv(filtered_df, output_path)

# Load symbols from .env.public file
load_dotenv(dotenv_path='.env.public')  # Specify path to .env.public explicitly
symbols = os.getenv('SYMBOLS', '').split(',')
if __name__ == '__main__':
    if not symbols or symbols == ['']:
        print("No symbols provided in the .env.public file under SYMBOLS.")
    else:
        date_str = get_current_date_string()
        file_types = [f'_{date_str}', '_0dte']
        for symbol in symbols:
            success_all = True
            for file_suffix in file_types:
                success = process_csv(symbol, file_suffix)
                if not success:
                    print(f"Failed to process CSV file with suffix '{file_suffix}' for symbol {symbol}.")
                    success_all = False
            if success_all:
                print(f"All files processed successfully for symbol {symbol}.")