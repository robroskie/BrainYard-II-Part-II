import re
import gensim
import nltk
from nltk.tokenize import word_tokenize

from nltk.corpus import stopwords

from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import wordnet as wn
import string

import gensim
from gensim import corpora

import pickle

from collections import defaultdict



def loadModels():

    loaded_model = gensim.models.ldamodel.LdaModel.load('models/lda_model.model')



    topics = loaded_model.print_topics(num_words=2)
    for topic in topics:
     print(topic)

    file_to_read = open("dictionary.gensim", "rb")

    dictionary = pickle.load(file_to_read)

# key_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]

    list_of_keywords = defaultdict(list)

    word_pairs_cleaned = []

#Manually decide topic(s) for each of the word pairs identified using the LDA model
    for topic in topics:
        str = topic[1]
    # str = str.replace('+', ', ')





    regex = re.compile('[^a-zA-Z ]')
    #str = ''.join([i for i in topic[1] if not i.isdigit()])

    str = regex.sub('', topic[1])
    str = str.replace('  ', ', ')

    word_pairs_cleaned.append(str)

    for topic in word_pairs_cleaned:
        print('next topic')
        print(topic)

    list_of_keywords[12].append([word_pairs_cleaned[0], 'Web development'])
    list_of_keywords[8].append([word_pairs_cleaned[1], 'Web development'])
    list_of_keywords[17].append([word_pairs_cleaned[2], 'Types of images'])
    list_of_keywords[16].append([word_pairs_cleaned[3], 'Element and window sizing'])
    list_of_keywords[10].append([word_pairs_cleaned[4], 'Models'])
    list_of_keywords[22].append([word_pairs_cleaned[5], 'System task management'])
    list_of_keywords[23].append([word_pairs_cleaned[6], 'HTML elements'])
    list_of_keywords[15].append([word_pairs_cleaned[7], 'Files'])
    list_of_keywords[14].append([word_pairs_cleaned[8], 'User requests and authentication'])
    list_of_keywords[7].append([word_pairs_cleaned[9], 'Server testing'])
    list_of_keywords[24].append([word_pairs_cleaned[10], 'Tags'])
    list_of_keywords[19].append([word_pairs_cleaned[11], 'Variable names and types'])
    list_of_keywords[18].append([word_pairs_cleaned[12], 'PHP and related libraries'])
    list_of_keywords[4].append([word_pairs_cleaned[13], 'JAVA developement'])
    list_of_keywords[11].append([word_pairs_cleaned[14], 'Variable names and types'])
    list_of_keywords[21].append([word_pairs_cleaned[15], 'Static and dynamic binding'])
    list_of_keywords[9].append([word_pairs_cleaned[16], 'Android view class'])
    list_of_keywords[6].append([word_pairs_cleaned[17], 'HTML elements'])
    list_of_keywords[13].append([word_pairs_cleaned[18], 'Verson and builds'])
    list_of_keywords[1].append([word_pairs_cleaned[19], 'Events'])


    for kw in list_of_keywords:
        print(kw)

    return list_of_keywords, loaded_model, dictionary

def prepare_text_for_lda(text):
    tokens = word_tokenize(text)
    # tokens = [token for token in tokens if len(token) > 4]
    # tokens = [token for token in tokens if token not in en_stop]
    # tokens = [get_lemma(token) for token in tokens]
    return tokens

def removeFirstLastThree(text):
    text = text[3:]
    # text = text[:3]
    text = text[:len(text)-3]
    return text


def toLowerCase(text):
    text = [word.lower() for word in text]
    return text


def removeStopWords(text):
    stop_words=set(stopwords.words("english"))
    filtered_sent=[]
    for w in text:
        if w not in stop_words:
            filtered_sent.append(w)
    return filtered_sent



def applyPStemmer(text):
    ps = PorterStemmer()

    stemmed_words=[]
    for w in text:
        stemmed_words.append(ps.stem(w))

    return stemmed_words




# nltk.download('wordnet')


def get_lemma(text):
    words = []
    for word in text:
        lemma = wn.morphy(word)
        if (len(word) <= 2 or len(word) >= 15 or word == 'code' or word.isnumeric() or word == 'gt' or word == 'lt' or word =='quot' or word == 'pre' or word == 'amp'):
            continue 
        elif lemma is None or word == lemma:
            words.append(word)
        else:
            words.append(lemma)
    return words
from nltk.stem.wordnet import WordNetLemmatizer

def get_lemma2(word):
    return WordNetLemmatizer().lemmatize(word)






def getTopics(user_input):
    list_of_keywords, loaded_model, dictionary = loadModels()
    tokens = prepare_text_for_lda(user_input)
    tokens = removeFirstLastThree(tokens)
    tokens = toLowerCase(tokens)
    tokens = removeStopWords(tokens)
    tokens = applyPStemmer(tokens)
    tokens = get_lemma(tokens)

    new_doc = dictionary.doc2bow(tokens)

    matches = loaded_model.get_document_topics(new_doc)

    # print(loaded_model)
    # print(type(loaded_model.get_document_topics(new_doc)))
    # print(matches)

    matches.sort(key = lambda x: x[1], reverse = True)
 
    print('matches')
    print(matches)
    # print(type(matches))

    to_return = []



    for match in matches:
        print(type(match))
        print(match[0])
        if(match[1] > 0.4):
            print('******')
            print(match[0])
            print(list_of_keywords[match[0]])
            print('list_of_keywords[match[0]][1]')
            list_of_keywords = list(list_of_keywords[match[0]])
            to_return.append(list_of_keywords[match[0]])





    return to_return, list_of_keywords
