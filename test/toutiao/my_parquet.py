import fastparquet as fastparquet
import pandas as pd
from pandas.compat import pyarrow

# 写入 Parquet 文件
df = pd.DataFrame({'col1': [1, 2, 3], 'col2': ['a', 'b', 'c']})

# print(df.to_csv())
# df.to_parquet('example.parquet')
# pyarrow
# fastparquet


#
# # 读取 Parquet 文件
df = pd.read_parquet('example.parquet')
print(df)