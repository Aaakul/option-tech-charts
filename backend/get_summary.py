import os
import pandas as pd
from datetime import datetime

def load_csv(file_path):
    """
    Load a CSV file into a DataFrame.

    :param file_path: The path to the CSV file.
    :return: A pandas DataFrame containing the CSV data or None if an error occurs.
    """
    try:
        df = pd.read_csv(file_path)
        return df
    except FileNotFoundError:
        print(f"Error: The file {file_path} does not exist.")
        return None
    except pd.errors.EmptyDataError:
        print(f"Error: The file {file_path} is empty.")
        return None
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        return None

def check_required_columns(df, required_columns):
    """
    Check if all required columns are present in the DataFrame.

    :param df: The input DataFrame.
    :param required_columns: A list of required column names.
    :return: True if all required columns are present, False otherwise.
    """
    missing_columns = [column for column in required_columns if column not in df.columns]
    if missing_columns:
        raise ValueError(f'Missing columns: {", ".join(missing_columns)}')
    return True

def calculate_totals(group):
    """
    Calculate total open interest, delta, and gamma for call and put options within a group.

    :param group: A pandas GroupBy object.
    :return: A pandas Series with the calculated totals.
    """
    call_group = group[group['type'] == 'call']
    put_group = group[group['type'] == 'put']
    
    call_open_interest = call_group['open_interest'].sum()
    put_open_interest = put_group['open_interest'].sum()
    
    # multiplier 100
    call_delta = (call_group['delta'] * call_group['open_interest']).sum() * 100
    put_delta = (put_group['delta'] * put_group['open_interest']).sum() * 100
    call_gamma = (call_group['gamma'] * call_group['open_interest']).sum() * 100
    put_gamma = -(put_group['gamma'] * put_group['open_interest']).sum() * 100  # negative gamma
    
    # calculate net Delta, Gamma
    net_delta = call_delta + put_delta
    net_gamma = call_gamma + put_gamma  
    
    return pd.Series({
        'call_open_interest': call_open_interest,
        'put_open_interest': put_open_interest,
        'call_delta': call_delta.round(2),
        'put_delta': put_delta.round(2),
        'call_gamma': call_gamma.round(2),
        'put_gamma': put_gamma.round(2),
        'net_delta': net_delta.round(2),
        'net_gamma': net_gamma.round(2),
    })

def save_result_df(result_df, output_path):
    """
    Save the result DataFrame to a new CSV file.

    :param result_df: The result DataFrame to save.
    :param output_path: The path where the new CSV file will be saved.
    :return: True if the file was saved successfully, False otherwise.
    """
    try:
        result_df.to_csv(output_path, index=False)
        print(f"Summary has been saved to {output_path}")
        return True
    except Exception as e:
        print(f"An error occurred while saving the file: {e}")
        return False

def main(symbol):
    """
    Main function to execute the summary calculation process.

    :param symbol: The stock or option symbol to process.
    """
    # Define file paths
    now = datetime.now()
    input_file_name = f'{symbol}_{now.year}_{now.month}.csv'
    input_dir = f'./data/{symbol}'
    input_path = os.path.join(input_dir, input_file_name)

    # Load the CSV file into a DataFrame
    df = load_csv(input_path)
    if df is None:
        print("Failed to load the CSV file. Exiting.")
        return

    # Ensure all necessary columns are present
    required_columns = ['expiration', 'strike', 'type', 'open_interest', 'delta', 'gamma']
    check_required_columns(df, required_columns)

    # Calculate totals by strike
    result_df = df.groupby('strike').apply(calculate_totals).reset_index()

    # Create output directory if it doesn't exist
    os.makedirs(input_dir, exist_ok=True)

    # Define the output file name with year and month
    output_file_name = f'{symbol}_summary_{now.year}_{now.month}.csv'
    output_path = os.path.join(input_dir, output_file_name)

    # Save the result DataFrame to a new CSV file
    save_result_df(result_df, output_path)

if __name__ == "__main__":
    # Specify the symbol to process
    symbol = 'SPY'
    main(symbol)