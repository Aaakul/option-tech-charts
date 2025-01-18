import os
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