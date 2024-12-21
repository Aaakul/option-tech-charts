import os
from helper import load_csv, save_to_json, get_current_date_string

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

def main(symbol):
    """
    Main function to execute the JSON export process.

    :param symbol: The stock or option symbol to process.
    """
    # Define file paths
    date_str = get_current_date_string()
    input_file_name = f'{symbol}_filtered_{date_str}.csv'
    input_dir = f'./data/{symbol}'
    input_path = os.path.join(input_dir, input_file_name)

    # Load the CSV file into a DataFrame
    df = load_csv(input_path)
    if df is None:
        print("Failed to load the CSV file. Exiting.")
        return

    # Prepare the data for JSON export
    data = prepare_data(df)

    output_dir = f'./JSON/{symbol}'

    # Define the output file name with year and month
    output_file_name = f'{symbol}_data.json'
    output_path = os.path.join(output_dir, output_file_name)

    # Save the data to a JSON file
    save_to_json(data, output_path)

if __name__ == "__main__":
    # Specify the symbol to process
    symbol = 'SPY'
    main(symbol)