import os
import PyPDF2

folder_path = os.getcwd()
# 输出待转换文件夹的路径
print(folder_path)

# 遍历文件夹中的所有文件
for filename in os.listdir(folder_path):
    # 判断文件是否是 PDF 文件
    if filename.endswith('.pdf'):
        # 构造同名的 TXT 文件路径
        txt_path = os.path.join(folder_path, os.path.splitext(filename)[0] + '.txt')
        # 打开 PDF 文件，并创建一个新的 TXT 文件
        with open(os.path.join(folder_path, filename), 'rb') as pdf_file, open(txt_path, 'w', encoding='utf-8') as txt_file:
            # 创建 PDF 解析器对象
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            # 遍历 PDF 文件的所有页面
            for page_num in range(len(pdf_reader.pages)):
                # 获取页面对象
                page_obj = pdf_reader.pages[page_num]
                # 提取页面文本，并写入 TXT 文件
                page_text = page_obj.extract_textx()
                txt_file.write(page_text)
        print(f'{filename} has been converted to {os.path.basename(txt_path)}.')
