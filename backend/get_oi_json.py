import os
import pandas as pd
import json
from datetime import datetime

# 读取过滤后的CSV文件
symbol = 'SPY'  # 这里可以替换成其他标的物
input_file_name = f'{symbol}_filtered_{datetime.now().month}.csv'
input_path = f'./data/{symbol}/{input_file_name}'

df = pd.read_csv(input_path)


# 准备数据
data = []
for _, row in df.iterrows():
    strike = row['strike']
    call_open_interest = row['call_open_interest']
    put_open_interest = -row['put_open_interest']  # 转换为负值
    data.append({
        'strike': strike,
        'call_open_interest': call_open_interest,
        'put_open_interest': put_open_interest
    })

# 保存为JSON文件
output_dir = f'./JSON/{symbol}/'
os.makedirs(output_dir, exist_ok=True)

output_file_name = f'{symbol}_OI_chart_data.json'
output_path = os.path.join(output_dir, output_file_name)

with open(output_path, 'w') as json_file:
    json.dump(data, json_file, indent=4)

print(f"数据已导出到 {output_path}")