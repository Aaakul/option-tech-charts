import os
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

def main(symbol):
    """
    Main function to execute the summary calculation process.

    :param symbol: The stock or option symbol to process.
    """
    # Define file paths
    date_str = get_current_date_string()
    input_file_name = f'{symbol}_{date_str}.csv'
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

    # Calculate totals by strike, ensuring the 'strike' column is included in the result
    result_df = df.groupby('strike', as_index=False).apply(calculate_totals, include_groups=False)

    # Define the output file name with year and month
    output_file_name = f'{symbol}_summary_{date_str}.csv'
    output_path = os.path.join(input_dir, output_file_name)

    # Save the result DataFrame to a new CSV file
    save_to_csv(result_df, output_path)

if __name__ == "__main__":
    # Specify the symbol to process
    symbol = 'SPY'
    main(symbol)