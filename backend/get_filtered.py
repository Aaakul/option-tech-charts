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

    # Optionally, you can uncomment the following line to retain only specific columns
    # final_df = second_filtered_df[['strike', 'call_open_interest', 'put_open_interest', 'call_delta', 'put_delta', 'call_gamma', 'put_gamma']]
    
    return second_filtered_df

def save_filtered_data(filtered_df, output_path):
    """
    Save the filtered DataFrame to a new CSV file.

    :param filtered_df: The filtered DataFrame to save.
    :param output_path: The path where the new CSV file will be saved.
    :return: True if the file was saved successfully, False otherwise.
    """
    try:
        filtered_df.to_csv(output_path, index=False)
        print(f"Filtered data has been saved to {output_path}")
        return True
    except Exception as e:
        print(f"An error occurred while saving the file: {e}")
        return False

def main(symbol):
    """
    Main function to execute the data filtering process.

    :param symbol: The stock or option symbol to process.
    """
    # Define file paths
    now = datetime.now()
    input_file_name = f'{symbol}_summary_{now.year}_{now.month}.csv'
    input_dir = f'./data/{symbol}'
    input_path = os.path.join(input_dir, input_file_name)

    # Load the CSV file into a DataFrame
    df = load_csv(input_path)
    if df is None:
        print("Failed to load the CSV file. Exiting.")
        return

    # Filter the data
    filtered_df = filter_data(df)

    # Create output directory if it doesn't exist
    os.makedirs(input_dir, exist_ok=True)

    # Define the output file name with year and month
    output_file_name = f'{symbol}_filtered_{now.year}_{now.month}.csv'
    output_path = os.path.join(input_dir, output_file_name)

    # Save the filtered data to a new CSV file
    save_filtered_data(filtered_df, output_path)

if __name__ == "__main__":
    # Specify the symbol to process
    symbol = 'SPY'
    main(symbol)