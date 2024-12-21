import os
import pandas as pd
import json
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

def prepare_data(df):
    """
    Prepare the data for JSON export by converting the DataFrame to a list of dictionaries.

    :param df: The input DataFrame.
    :return: A list of dictionaries containing the prepared data.
    """
    # Convert put_open_interest to negative values
    df['put_open_interest'] = -df['put_open_interest']

    # Select and rename columns for the JSON output
    data = df[['strike', 'call_open_interest', 'put_open_interest', 'call_delta', 'put_delta', 
               'call_gamma', 'put_gamma', 'net_delta', 'net_gamma']].to_dict(orient='records')
    
    return data

def save_to_json(data, output_path):
    """
    Save the prepared data to a JSON file.

    :param data: A list of dictionaries containing the prepared data.
    :param output_path: The path where the new JSON file will be saved.
    :return: True if the file was saved successfully, False otherwise.
    """
    try:
        with open(output_path, 'w') as json_file:
            json.dump(data, json_file, indent=4)
        print(f"Data has been exported to {output_path}")
        return True
    except Exception as e:
        print(f"An error occurred while saving the file: {e}")
        return False

def main(symbol):
    """
    Main function to execute the JSON export process.

    :param symbol: The stock or option symbol to process.
    """
    # Define file paths
    now = datetime.now()
    input_file_name = f'{symbol}_filtered_{now.year}_{now.month}.csv'
    input_dir = f'./data/{symbol}'
    input_path = os.path.join(input_dir, input_file_name)

    # Load the CSV file into a DataFrame
    df = load_csv(input_path)
    if df is None:
        print("Failed to load the CSV file. Exiting.")
        return

    # Prepare the data for JSON export
    data = prepare_data(df)

    # Create output directory if it doesn't exist
    output_dir = f'./JSON/{symbol}'
    os.makedirs(output_dir, exist_ok=True)

    # Define the output file name with year and month
    output_file_name = f'{symbol}_data.json'
    output_path = os.path.join(output_dir, output_file_name)

    # Save the data to a JSON file
    save_to_json(data, output_path)

if __name__ == "__main__":
    # Specify the symbol to process
    symbol = 'SPY'
    main(symbol)