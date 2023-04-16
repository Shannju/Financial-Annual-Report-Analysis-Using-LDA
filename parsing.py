import os

#预处理

# 获取当前运行脚本的绝对路径
abs_path = os.path.abspath(__file__)

# 获取当前脚本的父文件夹的绝对路径
parent_path = os.path.dirname(abs_path)
output_path = parent_path+r"\result"
file_path =  parent_path+r"\data"
dic_path = parent_path+r"\stop_dic"

txt_path = file_path+r"\txt"
keywords_path = dic_path+r"\dictionary.txt"

def clean_text(text):
    # 使用正则表达式删除非法字符
    cleaned_text = re.sub(r'[\x00-\x1F]+', '', text)
    return cleaned_text


def read_keywords(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        keywords = file.read().splitlines()
    return keywords

def contains_keyword(sentence, keywords):
    for keyword in keywords:
        if keyword in sentence:
            return True
    return False


def read_and_split_file(file_path, keywords_path):
    keywords = read_keywords(keywords_path)

    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
        content = content.replace('\n', ',')
        content = content.replace(' ', ',')
        # 去除形如(cid:3311)的字符组合
        content = re.sub(r'\(cid:\d+\)', '', content)
        # 使用正则表达式分割文本，包含中文标点
        sentences = re.split(r'[.,;!?。，；！？：]', content)
        sentences = [
            s.strip() for s in sentences
            if s.strip() and is_valid_sentence(s.strip()) and contains_keyword(s.strip(), keywords)
        ]
    return sentences



def is_valid_sentence(sentence):
    return bool(re.search(r'[\u4e00-\u9fa5]', sentence))

def process_folder(folder_path):
    # print(f"path in function ",folder_path)
    all_sentences = []

    for file_name in os.listdir(folder_path):
        if file_name.endswith('.txt'):
            file_path = os.path.join(folder_path, file_name)
            sentences = read_and_split_file(file_path,keywords_path)
            all_sentences.extend(sentences)
    return all_sentences

import os
import re
import pandas as pd

def process_folder(folder_path):
    # 创建一个空的DataFrame，列名为'content', 'chinese', 'year'
    df = pd.DataFrame(columns=['content', 'chinese', 'year'])

    for file_name in os.listdir(folder_path):
        if file_name.endswith('.txt'):
            file_path = os.path.join(folder_path, file_name)
            sentences = read_and_split_file(file_path, keywords_path)

            # 使用正则表达式提取中文字符和年份
            chinese = ''.join(re.findall(r'[\u4e00-\u9fff]+', file_name))
            year = ''.join(re.findall(r'\d{4}', file_name))

            for sentence in sentences:
                # 使用pandas.concat将每个句子、中文字符和年份添加到DataFrame中

                new_row = pd.DataFrame({'content': [clean_text(sentence)], 'chinese': [chinese], 'year': [year]})
                df = pd.concat([df, new_row], ignore_index=True)

    # 将DataFrame保存为一个Excel文件
    # df.to_excel('output.xlsx', index=False)

    return df



def write_to_file(sentences_array, output_file):
    with open(output_file, 'w', encoding='utf-8') as file:
        for sentence in sentences_array:
            cleaned_sentence = clean_text(sentence)  # 清理句子中的非法字符
            file.write(cleaned_sentence + '\n')



# 调用process_folder函数，并将结果存储为一个DataFrame
result_df = process_folder(txt_path)

# 将DataFrame保存为一个Excel文件
output_path = os.path.join(file_path,'output.xlsx')

# 将整理后的数据保存到Excel文件
result_df.to_excel(output_path, index=False)

