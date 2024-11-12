import os
import pandas as pd
from datetime import datetime

# 定义输入文件路径
symbol = 'SPY'  # 这里可以替换成其他标的物
input_file_name = f'{symbol}_{datetime.now().month}.csv'
input_path = f'./data/{symbol}/{input_file_name}'

# 读取CSV文件
df = pd.read_csv(input_path)

# 确保所有必要的列都在DataFrame中
required_columns = ['expiration', 'strike', 'type', 'open_interest', 'delta', 'gamma']
if not all(column in df.columns for column in required_columns):
    raise ValueError('输入文件缺少必要的列')

# 定义一个函数来计算call和put的总未平仓数、总Delta和总Gamma
def calculate_totals(group):
    call_group = group[group['type'] == 'call']
    put_group = group[group['type'] == 'put']
    
    call_open_interest = call_group['open_interest'].sum()
    put_open_interest = put_group['open_interest'].sum()
    
    # 合约乘数100
    call_delta = (call_group['delta'] * call_group['open_interest'] * 100).round(2).sum()
    put_delta = (put_group['delta'] * put_group['open_interest'] * 100).round(2).sum() # 不需要加上负号
    call_gamma = (call_group['gamma'] * call_group['open_interest'] * 100).round(2).sum()
    put_gamma = -(put_group['gamma'] * put_group['open_interest'] * 100).round(2).sum()  # 对put的gamma加上负号
    
    # 计算净Delta, Gamma
    net_delta = call_delta + put_delta
    net_gamma = call_gamma + put_gamma  
    
    return pd.Series({
        'call_open_interest': call_open_interest,
        'put_open_interest': put_open_interest,
        'call_delta': call_delta,
        'put_delta': put_delta,
        'call_gamma': call_gamma,
        'put_gamma': put_gamma,
        'net_delta': net_delta,
        'net_gamma': net_gamma,
    })

# 按strike分组并应用计算函数
result_df = df.groupby('strike').apply(calculate_totals).reset_index()

# 创建输出目录
output_dir = f'./data/{symbol}'
os.makedirs(output_dir, exist_ok=True)

# 定义输出文件名和路径
output_file_name = f'{symbol}_summary_{datetime.now().month}.csv'
output_path = os.path.join(output_dir, output_file_name)

# 导出计算结果到新的CSV文件
result_df.to_csv(output_path, index=False)

print(f"计算结果已保存到 {output_path}")