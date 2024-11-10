from datetime import datetime
import pandas as pd
import os

# 读取第一步生成的CSV文件
symbol = 'SPY'  # 这里可以替换成其他标的物
input_file_name = f'{symbol}_summary_{datetime.now().month}.csv'
input_path = f'./data/{symbol}/{input_file_name}'

# 读取CSV文件
df = pd.read_csv(input_path)

# 检查读取的DataFrame
print("读取的CSV文件内容:")
print(df.head())

# 定义收盘价为均值
close = 598
strike_mean = close

# 计算strike的标准差
strike_std = df['strike'].std()

# 计算1个标准差范围
# 68% range
lower_bound = strike_mean - 1 * strike_std
upper_bound = strike_mean + 1 * strike_std

# 筛选出trike在1个标准差范围内的数据
filtered_df = df[(df['strike'] >= lower_bound) & (df['strike'] <= upper_bound)]

# 计算put_open_interest和call_open_interest的标准差
# put_open_interest_std = filtered_df['put_open_interest'].std()
# call_open_interest_std = filtered_df['call_open_interest'].std()

# 计算put_open_interest和call_open_interest的下限值
put_open_interest_lower_bound = filtered_df['put_open_interest'].mean()
call_open_interest_lower_bound = filtered_df['call_open_interest'].mean()

# 筛选出put_open_interest大于其下限值或call_open_interest大于其下限值的数据
second_filtered_df = filtered_df[
    (filtered_df['put_open_interest'] > put_open_interest_lower_bound) |
    (filtered_df['call_open_interest'] > call_open_interest_lower_bound)
]

# 只保留需要的列
final_df = second_filtered_df[['strike',"call_open_interest","put_open_interest","call_delta","put_delta","call_gamma","put_gamma"]]

# 检查筛选后的DataFrame
print("筛选后的DataFrame:")
print(final_df.head())

# 创建输出目录
output_dir = f'./data/{symbol}'
os.makedirs(output_dir, exist_ok=True)

# 保存筛选后的数据到新的CSV文件
output_file_name = f'{symbol}_filtered_{datetime.now().month}.csv'
output_path = os.path.join(output_dir, output_file_name)
final_df.to_csv(output_path, index=False)

print(f"数据已筛选并保存到 {output_path}")