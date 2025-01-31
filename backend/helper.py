import os
from dotenv import load_dotenv
import pandas as pd
from datetime import datetime
import json

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

def save_to_csv(df, output_path):
    """
    Save the DataFrame to a new CSV file.

    :param df: The DataFrame to save.
    :param output_path: The path where the new CSV file will be saved.
    :return: True if the file was saved successfully, False otherwise.
    """
    try:
        df.to_csv(output_path, index=False)
        print(f"Data has been saved to {output_path}")
        return True
    except Exception as e:
        print(f"An error occurred while saving the file: {e}")
        return False

def save_to_json(data, output_path):
    """
    Save the data to a JSON file.

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
    else:
        return True

def create_output_directory(output_dir):
    """
    Create the output directory if it doesn't exist.

    :param output_dir: The path to the output directory.
    """
    os.makedirs(output_dir, exist_ok=True)

def get_current_date_string():
    """
    Get the current date string in the format YYYY_MM.

    :return: A string representing the current year and month.
    """
    now = datetime.now()
    return f"{now.year}_{now.month}"


def process_csv(func):
    """
    Function to process the data for predefined symbols and file suffixes.
    
    :param func: Function used to process DataFrame. 
    :return: True if the process was successful for all symbols and suffixes, False otherwise.
    """
    success_all = True
    # Load symbols from .env.public file
    load_dotenv(dotenv_path='.env.public')  # Specify path to .env.public explicitly
    symbols = os.getenv('SYMBOLS', '').split(',')
    if not symbols or symbols == ['']:
        print("No symbols provided in the .env.public file under SYMBOLS.")
        return False

    date_str = get_current_date_string()
    file_types = [f'_{date_str}', '_0dte']
    
    for symbol in symbols:
        for file_suffix in file_types:
            input_file_name = f'{symbol}_summary{file_suffix}.csv'
            input_dir = './data/{}'.format(symbol)
            input_path = os.path.join(input_dir, input_file_name)

            output_file_name = f'{symbol}_filtered{file_suffix}.csv'
            output_path = os.path.join(input_dir, output_file_name)

            # Load the CSV file into a DataFrame
            df = load_csv(input_path)
            if df is None:
                success_all = False
                print(f"Failed to load CSV file with suffix '{file_suffix}' for symbol {symbol}.")
                continue

            # Process the data
            processed_df = func(df)

            # Save the filtered data to a new CSV file
            if not save_to_csv(processed_df, output_path):
                success_all = False
                print(f"Failed to save processed CSV file with suffix '{file_suffix}' for symbol {symbol}.")

    return success_all