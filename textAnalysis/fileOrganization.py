import os
import re

# 指定PDF总文件夹路径
pdf_root_folder_path = 'E:\\filetest'

# 汉字数字映射表
chinese_num_map = {
    '零': '0', '一': '1', '二': '2', '三': '3', '四': '4',
    '五': '5', '六': '6', '七': '7', '八': '8', '九': '9'
}

# 将汉字数字转换为阿拉伯数字
def chinese_to_arabic(chinese_num):
    arabic_num = ''
    for char in chinese_num:
        arabic_num += chinese_num_map.get(char, '')
    return arabic_num

# 遍历总文件夹中的所有子文件夹
for stock_code_folder in os.listdir(pdf_root_folder_path):
    stock_code_folder_path = os.path.join(pdf_root_folder_path, stock_code_folder)
    if os.path.isdir(stock_code_folder_path):
        # 存储需要删除的文件
        files_to_delete = set()
        # 存储需要重命名的文件
        files_to_rename = {}
        # 存储每个年份的文件列表
        files_by_year = {}

        # 遍历子文件夹中的所有文件
        for file_name in os.listdir(stock_code_folder_path):
            if file_name.endswith('.pdf'):
                # 规则1和2：删除带有"ST"、"补充"和"更正"的PDF
                if "ST" in file_name or "补充" in file_name or "更正" in file_name or "取消" in file_name or "关于" in file_name:
                    files_to_delete.add(file_name)
                else:
                    year_match = re.search(r'(\d{4})年|([一二三四五六七八九零十百千万]{2,4})年', file_name)
                    if year_match:
                        if year_match.group(1):  # 匹配到阿拉伯数字年份
                            year = year_match.group(1)
                        else:  # 匹配到汉字年份
                            year = chinese_to_arabic(year_match.group(2))
                        # 添加到该年份的文件列表
                        if year not in files_by_year:
                            files_by_year[year] = []
                        files_by_year[year].append(file_name)

        # 处理每个年份的文件
        for year, files in files_by_year.items():
            # 如果该年份有多个文件
            if len(files) > 1:
                # 找到最后一个"更新"的文件
                last_updated_file = None
                for file_name in files:
                    if "更新" in file_name:
                        last_updated_file = file_name
                # 如果存在"更新"的文件，则删除其他文件
                if last_updated_file:
                    for file_name in files:
                        if file_name != last_updated_file:
                            files_to_delete.add(file_name)
                    new_name = year + '.pdf'
                    files_to_rename[last_updated_file] = new_name
                # 如果不存在"更新"的文件，则保留原名
            else:
                # 仅有一个文件，直接重命名
                file_name = files[0]
                new_name = year + '.pdf'
                files_to_rename[file_name] = new_name

        # 执行删除
        for file_name in files_to_delete:
            file_path = os.path.join(stock_code_folder_path, file_name)
            if os.path.exists(file_path):
                os.remove(file_path)

        # 执行重命名
        for old_name, new_name in files_to_rename.items():
            old_path = os.path.join(stock_code_folder_path, old_name)
            new_path = os.path.join(stock_code_folder_path, new_name)
            if os.path.exists(old_path) and not os.path.exists(new_path):
                os.rename(old_path, new_path)

print('PDF文件整理完成。')