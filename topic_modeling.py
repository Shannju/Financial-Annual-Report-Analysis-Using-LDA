import os
import pandas as pd
import re
import jieba
import jieba.posseg as psg

#预处理
data=pd.read_excel("output.xlsx")#content type
# 获取当前运行脚本的绝对路径
abs_path = os.path.abspath(__file__)

# 获取当前脚本的父文件夹的绝对路径
parent_path = os.path.dirname(abs_path)

doc_path = parent_path+r"\sentences.txt"

output_path = parent_path+r"\result"
file_path =  parent_path+r"\data"
os.chdir(file_path)



os.chdir(output_path)
dic_file =  parent_path+r"\stop_dic\dict.txt"
stop_file = parent_path+r"\stop_dic\stopwords.txt"

with open(doc_path, encoding='utf-8') as file:
    # rest of your code here
    docs = [line.strip() for line in file.readlines()]



def chinese_word_cut(mytext):
    jieba.load_userdict(dic_file)
    jieba.initialize()
    try:
        stopword_list = open(stop_file,encoding ='utf-8')
    except:
        stopword_list = []
        print("error in stop_file")
    stop_list = []
    flag_list = ['n','nz','vn']
    for line in stopword_list:
        line = re.sub(u'\n|\\r', '', line)
        stop_list.append(line)
    
    word_list = []
    #jieba分词
    seg_list = psg.cut(mytext)
    for seg_word in seg_list:
        word = re.sub(u'[^\u4e00-\u9fa5]','',seg_word.word)
        # word = seg_word.word  #如果想要分析英语文本，注释这行代码，启动下行代码
        find = 0
        for stop_word in stop_list:
            if stop_word == word or len(word)<2:     #this word is stopword
                    find = 1
                    break
        if find == 0 and seg_word.flag in flag_list:
            word_list.append(word)
    return (" ").join(word_list)



# data["content"] = docs
data["content_cutted"] = data.content.apply(chinese_word_cut)
# ## 2.LDA分析

# In[37]:


from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation


# In[38]:


def print_top_words(model, feature_names, n_top_words):
    tword = []
    for topic_idx, topic in enumerate(model.components_):
        print("Topic #%d:" % topic_idx)
        topic_w = " ".join([feature_names[i] for i in topic.argsort()[:-n_top_words - 1:-1]])
        tword.append(topic_w)
        print(topic_w)
    return tword


# In[39]:


n_features = 1000 #提取1000个特征词语
tf_vectorizer = CountVectorizer(strip_accents = 'unicode',
                                max_features=n_features,
                                stop_words='english',
                                max_df = 0.5,
                                min_df = 10                                )
tf = tf_vectorizer.fit_transform(data.content_cutted)


# In[40]:


n_topics = 5 # 主题数量！
#max_iter 迭代次数 可以增减
#alpha beta可以省略 由模型来确定
lda = LatentDirichletAllocation(n_components=n_topics, max_iter=5,
                                learning_method='batch',
                                learning_offset=50,
                                # doc_topic_prior=0.1,#alpha
                                # topic_word_prior=0.01,#beta
                               random_state=0)
lda.fit(tf)


# ### 2.1输出每个主题对应词语

# In[11]:

#主题的名字需要自定义了
n_top_words = 15
tf_feature_names = tf_vectorizer.get_feature_names_out()
topic_word = print_top_words(lda, tf_feature_names, n_top_words)


# ### 2.2输出每篇文章对应主题

# In[12]:


import numpy as np


# In[13]:


topics=lda.transform(tf)


# In[28]:


topic = []
for t in topics:
    topic.append("Topic #"+str(list(t).index(np.max(t))))
data['概率最大的主题序号']=topic
data['每个主题对应概率']=list(topics)
data.to_excel("data_topic.xlsx",index=False)


# ### 2.3可视化

# In[29]:


import pyLDAvis
import pyLDAvis.sklearn


# In[31]:

pic = pyLDAvis.sklearn.prepare(lda, tf, tf_vectorizer)
#pyLDAvis.display(pic)
pyLDAvis.save_html(pic, 'lda_pass'+str(n_topics)+'.html')
#pyLDAvis.display(pic)
#去工作路径下找保存好的html文件
#和视频里讲的不一样，目前这个代码不需要手动中断运行，可以快速出结果


# ### 2.4困惑度

# In[32]:


import matplotlib.pyplot as plt


# In[41]:
#困惑度 可以看出主题数量哪个最合适

plexs = []
scores = []
n_max_topics = 16
for i in range(1,n_max_topics):
    print(i)
    lda = LatentDirichletAllocation(n_components=i, max_iter=50,
                                    learning_method='batch',
                                    learning_offset=50,random_state=0)
    lda.fit(tf)
    plexs.append(lda.perplexity(tf))
    scores.append(lda.score(tf))


# In[42]:


n_t=15#区间最右侧的值。注意：不能大于n_max_topics
x=list(range(1,n_t+1))
plt.plot(x,plexs[0:n_t])
plt.xlabel("number of topics")
plt.ylabel("perplexity")
plt.show()


# In[ ]:




