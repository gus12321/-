import os
import jieba
import pandas as pd
from collections import Counter

# 设置文本文件夹的路径
folder_path = 'E:\\TxtData'

# 定义需要统计词频的词汇
keywords = ['创新', '创造力', '开拓']

# 准备一个空的DataFrame来存储结果
# 每个关键词都有自己的列
columns = ['股票代码', '年份'] + keywords
results_df = pd.DataFrame(columns=columns)

# 遍历文件夹中的所有子文件夹（股票代码）
for subfolder in os.listdir(folder_path):
    subfolder_path = os.path.join(folder_path, subfolder)
    if os.path.isdir(subfolder_path):
        # 遍历子文件夹中的所有txt文件（年报）
        for filename in os.listdir(subfolder_path):
            if filename.endswith('.txt'):
                year = filename.split('.')[0]  # 文件名是年份
                file_path = os.path.join(subfolder_path, filename)
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                    # 使用jieba进行分词
                    words = jieba.lcut(content)
                    # 统计关键词的词频
                    word_count = Counter(words)
                    # 创建一个新行的字典
                    row_data = {'股票代码': subfolder, '年份': year}
                    # 添加每个关键词的频数到新行字典
                    for keyword in keywords:
                        row_data[keyword] = word_count[keyword]
                    # 将新行添加到DataFrame
                    results_df = results_df._append(row_data, ignore_index=True)

# 将DataFrame保存到Excel文件
results_df.to_excel('annual_reports_keyword_frequency1.xlsx', index=False)