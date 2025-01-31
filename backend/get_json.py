import os

from dotenv import load_dotenv
from helper import create_output_directory, load_csv, save_to_json, get_current_date_string

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

def main(symbol, file_suffix):
    """
    Main function to execute the JSON export process.

    :param file_suffix: The suffix of the file name indicating its type.
    :return: True if successful, False otherwise.
    """
    # Define file paths
    input_file_name = f'{symbol}_filtered{file_suffix}.csv'
    input_dir = f'./data/{symbol}'
    input_path = os.path.join(input_dir, input_file_name)

    output_dir = os.path.join('./JSON', symbol)
    output_file_name = f'{symbol}_0dte.json' if file_suffix == '_0dte' else f'{symbol}_month.json'
    output_path = os.path.join(output_dir, output_file_name)

    # Load the CSV file
    df = load_csv(input_path)
    if df is None:
        return False

    # Prepare the data for JSON export
    data = prepare_data(df)

    # Ensure the output directory exists
    create_output_directory(output_dir)

    # Save the data to a JSON file
    return save_to_json(data, output_path)

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
                success = main(symbol, file_suffix)
                if not success:
                    print(f"Failed to process CSV file with suffix '{file_suffix}' for symbol {symbol}.")
                    success_all = False
            if success_all:
                print(f"All files processed successfully for symbol {symbol}.")