import fitz  # PyMuPDF
import os
import re

# 指定包含PDF年报的股票代码子文件夹的总文件夹路径
pdf_root_folder_path = 'E:\\filetest'
# 指定保存TXT文件的总文件夹路径
txt_root_folder_path = 'E:\\TxtData'

# 确保TXT总文件夹存在
os.makedirs(txt_root_folder_path, exist_ok=True)

# 遍历总文件夹中的所有股票代码子文件夹
for stock_code_folder in os.listdir(pdf_root_folder_path):
    stock_code_folder_path = os.path.join(pdf_root_folder_path, stock_code_folder)
    if os.path.isdir(stock_code_folder_path):
        # 在TXT总文件夹中创建对应的股票代码子文件夹
        txt_stock_code_folder_path = os.path.join(txt_root_folder_path, stock_code_folder)
        os.makedirs(txt_stock_code_folder_path, exist_ok=True)

        # 遍历子文件夹中的所有PDF文件
        for pdf_file in os.listdir(stock_code_folder_path):
            if pdf_file.endswith('.pdf'):
                # 构建完整的PDF文件路径
                pdf_path = os.path.join(stock_code_folder_path, pdf_file)
                # 打开PDF文件
                pdf = fitz.open(pdf_path)
                # 读取PDF文件的每一页
                text = ''
                for page in pdf:
                    text += page.get_text()
                pdf.close()

                # 构建TXT文件的名称和路径
                txt_file_name = os.path.splitext(pdf_file)[0] + '.txt'
                txt_path = os.path.join(txt_stock_code_folder_path, txt_file_name)

                # 将提取的文本保存到TXT文件
                with open(txt_path, 'w', encoding='utf-8') as txt_file:
                    txt_file.write(text)

print('PDF转换完成。')