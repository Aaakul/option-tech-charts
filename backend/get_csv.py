import os
from dotenv import load_dotenv
import requests
from helper import create_output_directory

# Load API key from .env file
load_dotenv()  # Loads the default .env file for API key
api_key = os.getenv("ALPHA_VANTAGE_API_KEY")

# Load symbols from .env.public file
load_dotenv(dotenv_path='.env.public')  # Specify path to .env.public explicitly
symbols = os.getenv('SYMBOLS', '').split(',')

# Constants for default values and paths
DEFAULT_SAVE_DIR = './data'

def download_csv(symbol, api_key, save_dir=None):
    """
    Download a CSV file from the Alpha Vantage API and save it to a specified directory.

    :param symbol: The stock symbol for which to download historical options data.
    :param api_key: Your Alpha Vantage API key.
    :param save_dir: Optional; the directory where the CSV file will be saved. 
                     If not provided, defaults to './data/<symbol>'.
    :return: True if the download was successful, False otherwise.
    """
    # Check if the API key is set
    if api_key is None:
        print("API key is not set.")
        return False

    # Determine the save directory
    if save_dir is None:
        save_dir = os.path.join(DEFAULT_SAVE_DIR, symbol)
    else:
        save_dir = os.path.join(save_dir, symbol)

    # Construct the API URL (hardcoded as per request)
    url = f'https://www.alphavantage.co/query?function=HISTORICAL_OPTIONS&symbol={symbol}&apikey={api_key}&datatype=csv'
    
    # Create output directory if it doesn't exist
    create_output_directory(save_dir)

    # Define the file path to save the CSV
    file_path = os.path.join(save_dir, f'historical_options_{symbol}.csv')

    try:
        # Send GET request to the API
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors

        # Write the response content to the file
        with open(file_path, 'wb') as file:
            file.write(response.content)

        print(f'Successfully saved {file_path}')
        return True
    except requests.exceptions.RequestException as e:
        print(f'An error occurred while downloading the CSV: {e}')
        return False

if __name__ == '__main__':
    if not symbols or symbols == ['']:
        print("No symbols provided in the .env.public file under SYMBOLS.")
    elif api_key is None:
        print("API key not found in the .env file.")
    else:
        for symbol in symbols:
            success = download_csv(symbol.strip(), api_key)
            if not success:
                print(f"Failed to download CSV file for symbol {symbol}.")