import numpy as np
import os
import pandas as pd
import re
import jieba
import jieba.posseg as psg


#预处理

# 获取当前运行脚本的绝对路径
abs_path = os.path.abspath(__file__)

# 获取当前脚本的父文件夹的绝对路径
parent_path = os.path.dirname(abs_path)

txt_path = parent_path+r"\txt"
# print("当前脚本的txt文件夹的绝对路径为：", txt_path)



def is_valid_sentence(sentence):
    return bool(re.search(r'[\u4e00-\u9fa5]', sentence))

def read_and_split_file(file_path):

    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
        # 去除换行符
        content = content.replace('\n', ' ')
        # 去除形如(cid:3311)的字符组合
        content = re.sub(r'\(cid:\d+\)', '', content)
        # 使用正则表达式分割文本，包含中文标点
        sentences = re.split(r'[.,;!?。，；！？：]', content)
        # 去除前后空格并过滤无效句子
        sentences = [s.strip() for s in sentences if s.strip() and is_valid_sentence(s.strip())]
    return sentences

def process_folder(folder_path):
    # print(f"path in function ",folder_path)
    all_sentences = []

    for file_name in os.listdir(folder_path):
        if file_name.endswith('.txt'):
            file_path = os.path.join(folder_path, file_name)
            sentences = read_and_split_file(file_path)
            all_sentences.extend(sentences)
    return all_sentences

def write_to_file(sentences_array, output_file):
    with open(output_file, 'w', encoding='utf-8') as file:
        for sentence in sentences_array:
            file.write(sentence + '\n')



sentences_array = process_folder(txt_path)
# print(sentences_array)
output_file = 'sentences.txt'
write_to_file(sentences_array, output_file)