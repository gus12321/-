import jieba
import os

# 指定文件夹路径
folder_path = 'E:\\TxtData\\000002'
# 创建一个新的子文件夹用于存放处理后的文件
output_folder = os.path.join(folder_path, 'marked_files')
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# 遍历文件夹中的所有文件
for filename in os.listdir(folder_path):
    # 检查文件扩展名是否为.txt
    if filename.endswith('.txt'):
        # 构建完整的文件路径
        file_path = os.path.join(folder_path, filename)

        # 读取文本文件
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        # 使用jieba进行分词，并获取每个词的起止位置
        words = jieba.tokenize(content)

        # 初始化一个新的内容字符串，用于存储带标注的文本
        new_content = ''
        last_end = 0

        # 遍历所有词语及其位置
        for word, start, end in words:
            # 如果找到关键词“创新”，则在其前后添加标注
            if word == '创新':
                new_content += content[last_end:start] + '**创新**'
                last_end = end
            else:
                new_content += content[last_end:end]
                last_end = end

        # 将最后一个词语之后的内容也加入到新内容中
        new_content += content[last_end:]

        # 构建新文件的路径，保存在子文件夹中
        new_file_path = os.path.join(output_folder, filename)

        # 将带有标注的新内容写入一个新的txt文件
        with open(new_file_path, 'w', encoding='utf-8') as file:
            file.write(new_content)

        print(f'文件{filename}已处理，标注完成。新文件保存在：{new_file_path}')