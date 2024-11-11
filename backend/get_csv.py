import os
import requests

api_key = os.getenv("ALPHA_VANTAGE_API_KEY")
symbol = 'SPY'

def download_csv(symbol, api_key, save_dir=f'./data/{symbol}'):
    # 构建API URL
    url = f'https://www.alphavantage.co/query?function=HISTORICAL_OPTIONS&symbol={symbol}&apikey={api_key}&datatype=csv'
    
    # 创建保存目录
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    
    # 定义文件保存路径
    file_path = os.path.join(save_dir, f'historical_options_{symbol}.csv')
    
    try:
        # 发送GET请求
        response = requests.get(url)
        response.raise_for_status()  # 检查请求是否成功
        
        # 将数据写入文件
        with open(file_path, 'wb') as file:
            file.write(response.content)
        
        print(f'Saved historical_options_{symbol}.csv')
    except requests.exceptions.RequestException as e:
        print(f'An error occurred: {e}')

download_csv(symbol, api_key)