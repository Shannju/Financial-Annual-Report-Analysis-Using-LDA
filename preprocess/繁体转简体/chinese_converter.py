import os
import opencc

# 初始化 OpenCC 转换器
converter = opencc.OpenCC('t2s.json')

import os

# 获取当前脚本的运行路径
current_path = os.getcwd()

folder_path = current_path
# 输出待转换文件夹的路径
print(folder_path)

# 获取文件夹中所有 .txt 文件的路径
file_paths = [os.path.join(folder_path, file) for file in os.listdir(folder_path) if file.endswith('.txt')]

# 遍历文件路径，逐个读取并转换文件内容
for file_path in file_paths:
    print(file_path)
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        # print(content)
        content = converter.convert(content)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
