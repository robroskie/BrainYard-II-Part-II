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
    # for topic in topics:
    #  print(topic)

    file_to_read = open("dictionary.gensim", "rb")

    dictionary = pickle.load(file_to_read)

# key_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]

    # list_of_keywords = defaultdict(list)
    list_of_keywords = [None] * 25
    word_pairs = []
    word_pairs_cleaned = []
    # print('length of list')
    # print(len(list_of_keywords))
#Manually decide topic(s) for each of the word pairs identified using the LDA model
    for topic in topics:
        # print('topic is {}'.format(topic))
        # str = topic[1]
        # print(type(topic))
        word_pairs.append(list(topic))
    # str = str.replace('+', ', ')

    # print(word_pairs)

    word_pairs_sorted = sorted(word_pairs, key = lambda x: x[0])

    # print(word_pairs_sorted)

    regex = re.compile('[^a-zA-Z ]')
    #str = ''.join([i for i in topic[1] if not i.isdigit()])

    for element in word_pairs_sorted:
        # print('element is.{}'.format(element))
        word_pairs = regex.sub('', element[1])
        word_pairs = word_pairs.replace('  ', ', ')

        word_pairs_cleaned.append([element[0], word_pairs])

    # for topic in word_pairs_cleaned:
        # print('next topic')
        # print(topic)

    list_of_keywords[0] = ''
    list_of_keywords[2] = ''
    list_of_keywords[3] = ''
    list_of_keywords[5] = ''

    list_of_keywords[1] = [word_pairs_cleaned[0], 'CSS Styling']
    list_of_keywords[4] = [word_pairs_cleaned[1], 'Server testing']
    list_of_keywords[6] = [word_pairs_cleaned[2], 'Arrays and lists']
    list_of_keywords[7] = [word_pairs_cleaned[3], 'Functions, methods and variables']
    list_of_keywords[8] = [word_pairs_cleaned[4], 'Files']
    list_of_keywords[9] = [word_pairs_cleaned[5], 'System task management']
    list_of_keywords[10] = [word_pairs_cleaned[6], 'JAVA developement']
    list_of_keywords[11] = [word_pairs_cleaned[7], 'Android view class']
    list_of_keywords[12] = [word_pairs_cleaned[8], 'Accessing and declaring variables']
    list_of_keywords[13] = [word_pairs_cleaned[9], 'Database queries']
    list_of_keywords[14] = [word_pairs_cleaned[10], 'Static and dynamic binding']
    list_of_keywords[15] = [word_pairs_cleaned[11], 'Verson and builds']
    list_of_keywords[16] = [word_pairs_cleaned[12], 'HTML elements']
    list_of_keywords[17] = [word_pairs_cleaned[13], 'Types of images']
    list_of_keywords[18] = [word_pairs_cleaned[14], 'Protocol/network stacks']
    list_of_keywords[19] = [word_pairs_cleaned[15], 'HTTP and TCP/IP']
    list_of_keywords[21] = [word_pairs_cleaned[16], 'Software models and development life cycle']
    list_of_keywords[22] = [word_pairs_cleaned[17], 'Primitive and reference data types']
    list_of_keywords[23] = [word_pairs_cleaned[18], 'Application tags and metadata']
    list_of_keywords[24] = [word_pairs_cleaned[19], 'HTML elements']


    # for kw in list_of_keywords:
        # print(kw)

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
 
    # print('matches')
    print(matches)
    print(type(matches))

    to_return_strong = []
    to_return_weak = []


    for match in matches:
        temp = list(match)

        # print(type(match))
        print('temp is {}'.format(temp))
        if(match[1] > 0.3):
            to_return_strong.append(list_of_keywords[match[0]][1])

        elif(match[1] < 0.3 and match[1] > 0.1):
            to_return_weak.append(list_of_keywords[match[0]][1])
        
    print('Stringly related to')
    print(to_return_strong)
    print('Weakly related to')
    print(to_return_weak)



    return to_return_strong, to_return_weak
