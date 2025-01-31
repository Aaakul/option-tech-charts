import os
from dotenv import load_dotenv
import pandas as pd
from helper import load_csv, save_to_csv, check_required_columns, get_current_date_string
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
    
    # Multiplier 100
    call_delta = (call_group['delta'] * call_group['open_interest']).sum() * 100
    put_delta = (put_group['delta'] * put_group['open_interest']).sum() * 100
    call_gamma = (call_group['gamma'] * call_group['open_interest']).sum() * 100
    put_gamma = -(put_group['gamma'] * put_group['open_interest']).sum() * 100  # Negative gamma
    
    # Calculate Net Delta, Gamma
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

def process_csv(symbol, file_suffix):
    """
    Process a specific type of CSV file for a given symbol.

    :param symbol: The stock or option symbol to process.
    :param file_suffix: The suffix of the file name indicating its type.
    :return: True if successful, False otherwise.
    """
    input_file_name = f'{symbol}{file_suffix}.csv'
    output_file_name = f'{symbol}_summary{file_suffix}.csv'
    input_dir = f'./data/{symbol}'
    input_path = os.path.join(input_dir, input_file_name)
    output_path = os.path.join(input_dir, output_file_name)

    df = load_csv(input_path)
    if df is None:
        return False

    # Ensure all necessary columns are present
    required_columns = ['expiration', 'strike', 'type', 'open_interest', 'delta', 'gamma']
    check_required_columns(df, required_columns)

    # Calculate totals by strike
    result_df = df.groupby('strike', as_index=False).apply(calculate_totals, include_groups=False)

    # Save the result DataFrame to a new CSV file
    return save_to_csv(result_df, output_path)

if __name__ == '__main__':
    load_dotenv(dotenv_path='.env.public')
    symbols = os.getenv('SYMBOLS', '').split(',')
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