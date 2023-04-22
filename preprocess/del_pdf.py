import os
# 获取当前脚本的运行路径
current_path = os.getcwd()

folder_path = current_path
# 输出待转换文件夹的路径
print(folder_path)

# 遍历文件夹中的所有文件
for filename in os.listdir(folder_path):
    # 判断文件是否是 PDF 文件
    if filename.endswith('.pdf'):
        # 构造同名的 TXT 文件路径
        txt_path = os.path.join(folder_path, os.path.splitext(filename)[0] + '.txt')
        # 判断 TXT 文件是否存在
        if os.path.exists(txt_path):
            # 如果存在，删除 PDF 文件
            pdf_path = os.path.join(folder_path, filename)
            os.remove(pdf_path)
            print(f'{pdf_path} has been removed.')
