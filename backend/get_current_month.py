import pandas as pd
from datetime import datetime, timedelta
import os

# 获取当前月份的第一个和最后一个日期
def get_month_dates():
    today = datetime.now()
    first_day_of_month = today.replace(day=1)
    if today.month == 12:
        next_month = today.replace(year=today.year + 1, month=1, day=1)
    else:
        next_month = today.replace(month=today.month + 1, day=1)
    last_day_of_month = next_month - timedelta(days=1)
    return first_day_of_month.strftime('%Y-%m-%d'), last_day_of_month.strftime('%Y-%m-%d')

# 读取CSV文件
symbol = 'SPY'  # 这里可以替换成其他标的物
file_name = f'./data/{symbol}/historical_options_{symbol}.csv'
df = pd.read_csv(file_name)


# 获取本月的第一个和最后一个日期
first_day_of_month, last_day_of_month = get_month_dates()

# 筛选条件
filtered_df = df[(df['expiration'] >= first_day_of_month) & 
                 (df['expiration'] <= last_day_of_month) & 
                 (df['delta'].abs() > 0.05) & 
                 (df['open_interest'] > 0)]

# 只保留需要的列
filtered_df = filtered_df[['expiration', 'strike', 'type', 'open_interest', 'implied_volatility', 'delta', 'gamma']]

# 创建输出目录
output_dir = f'./data/{symbol}'
os.makedirs(output_dir, exist_ok=True)

# 保存筛选后的数据到新的CSV文件
output_file_name = f'{symbol}_{datetime.now().month}.csv'
output_path = os.path.join(output_dir, output_file_name)
filtered_df.to_csv(output_path, index=False)

print(f"数据已筛选并保存到 {output_path}")
