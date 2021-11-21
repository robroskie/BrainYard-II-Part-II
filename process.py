import pyodbc 
import nltk
# nltk.download('stopwords')


import re
import numpy as np
import pandas as pd
from pprint import pprint

# Gensim
import gensim
import gensim.corpora as corpora
from gensim.utils import simple_preprocess
from gensim.models import CoherenceModel

# spacy for lemmatization
import spacy

# Plotting tools
# import pyLDAvis
# import pyLDAvis.gensim  # don't skip this
# import matplotlib.pyplot as plt
# %matplotlib inline
import processHelper as PH

def csim(data):
    print('working')




conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=.;DATABASE=StackOverflow;Trusted_Connection=yes;')
cursor = conn.cursor()




query = 'SELECT * FROM dbo.Posts tablesample(.1 percent)'

# res = cursor.execute(query)

#res = pd.read_sql(query, conn)
#print(len(res.index))
# print(res)
# sample = sample.loc[3]

# data = res.Body.values.tolist()

#res.to_csv('randomPosts.csv', encoding='utf-8', index=False)


print('done')

df = pd.read_csv('randomPosts.csv', encoding='utf-8')



#PH.processFile('RandomPosts.csv', 'RandomPosts')

print(df.Body)


df10 = df.Body


import spacy
from spacy.lang.en import English

import nltk
from nltk.tokenize import word_tokenize
# nltk.download('punkt')

parser = English()
nlp = spacy.load("en_core_web_sm")

a = word_tokenize('happy clam')
print(a)

print(type(df.Body))


# a = word_tokenize(df['Body'])

# tokens = df['Body'].apply(word_tokenize)


df = df[df['Body'].notna()]

# df['words_tokenized'] = word_tokenize(str(df['Body']))

# for element in df['Body']:
    # print(element)
    # print(type(element))
    # if(type(element) == float):
        # continue
    # word_tokenize(element)

# for i, row in df.iterrows():
    # ifor_val = word_tokenize(row.Body)

    # df.at[i,'words_tokenized'] = ifor_val
    
# print(df.head())

dict = df.to_dict('index')

for key in dict:
    # print(key)
    dict[key]['words_tokenized'] = word_tokenize(dict[key]['Body'])