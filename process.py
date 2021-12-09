import re
import gensim
import pickle
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.corpus import wordnet as wn
import pandas as pd
pd.options.mode.chained_assignment = None 

load_gensim_model = gensim.models.ldamodel.LdaModel.load('models/lda_model.model')
topics = load_gensim_model.print_topics(num_words=2)

file_to_read = open("models/dictionary.gensim", "rb")
dictionary = pickle.load(file_to_read)




def loadModels():
    word_pairs = []
    word_pairs_cleaned = []

    #Manually decide topic(s) for each of the word pairs identified using the LDA model
    for topic in topics:
        word_pairs.append(list(topic))

    word_pairs_sorted = sorted(word_pairs, key = lambda x: x[0])

    regex = re.compile('[^a-zA-Z ]')

    for element in word_pairs_sorted:
        word_pairs = regex.sub('', element[1])
        word_pairs = word_pairs.replace('  ', ', ')
        word_pairs_cleaned.append([element[0], word_pairs])
        print(word_pairs)

    return word_pairs_cleaned

def getKeywords(word_pairs_cleaned):
    list_of_keywords = [None] * 25

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

    return list_of_keywords

def prepare_LDA(text):
    tokens = word_tokenize(text)
    return tokens

def removeFirstLastThree(text):
    text = text[3:]
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





list_of_keywords = []

def getTopics(user_input):
    word_pairs_cleaned = loadModels()
    

    tokens = prepare_LDA(user_input)
    tokens = removeFirstLastThree(tokens)
    tokens = toLowerCase(tokens)
    tokens = removeStopWords(tokens)
    tokens = applyPStemmer(tokens)
    tokens = get_lemma(tokens)

    new_doc = dictionary.doc2bow(tokens)

    matches = load_gensim_model.get_document_topics(new_doc)



    matches.sort(key = lambda x: x[1], reverse = True)
 
 
    print(matches)
    print(type(matches))

    to_return = []


    for match in matches:
        temp = list(match)

  
        print('temp is {}'.format(temp))
        if(match[1] > 0.1):
            to_return.append(list_of_keywords[match[0]][1])



    

    return to_return


# print(getTopics('hello'))

 










 
def removeFirstLastThree(text):
    text = text[3:]
    text = text[:len(text)-3]
    return text


def applyPStemmer_df(text):

    ps = PorterStemmer()

    stemmed_words=[]

    for w in text:
        stemmed_words.append(ps.stem(w))

    return stemmed_words





def prepare_LDA_df(text):

    return word_tokenize(text)


def removeStopWords(text):
    stop_words=set(stopwords.words("english"))

    cleaned = []

    for word in text:
        if word not in stop_words:
            cleaned.append(word)
    return text


def get_lemma_df(text):
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



def prepareText(df):


    df['Body'] = df['Body'].astype(str)
    df['Body_processed'] = df.apply(lambda x: removeFirstLastThree(x['Body']), axis=1)

    df['Body_processed'] = df.apply(lambda x: prepare_LDA_df(x['Body_processed']), axis=1)

    df['Body_processed'] = df.apply(lambda x: applyPStemmer_df(x['Body_processed']), axis=1)

    df['Body_processed'] = df.apply(lambda x: removeStopWords(x['Body_processed']), axis=1)

    df['Body_processed'] = df.apply(lambda x: get_lemma_df(x['Body_processed']), axis=1)


    return df


df = pd.read_csv('randomPosts.csv', encoding='utf-8')




# Run function




df = prepareText(df.head(20))



# df.to_csv('Body_processed.csv', encoding='utf-8')

# --------- segment



word_pairs_cleaned = loadModels()
list_of_keywords = getKeywords(word_pairs_cleaned)



df['Body_processed_topics'] = df.apply(lambda x: dictionary.doc2bow(x['Body_processed']), axis=1)

df['Body_processed_topics'] = df.apply(lambda x: load_gensim_model.get_document_topics(x['Body_processed_topics']), axis=1)


print('**********')
# print(list_of_keywords)


def sorterTopThree(nums):
    print(nums)
    nums.sort(key = lambda x: x[1], reverse = True)
    print(nums[:3])
    return nums[:3]
    

df['Body_processed_topics_sorted'] = df.apply(lambda x: sorterTopThree(x['Body_processed_topics']), axis=1)




# def getTopicsfromKwrds(keywords):
#     to_return = []
#     i = 0

#     for match in keywords:
 
#         temp = list(match)
        
     
#         if(list_of_keywords[temp[0]]):
#                 if(temp[1] > 0.1):
#                     to_return.append(list_of_keywords[temp[0]][1])
#                     print('temp is {}'.format(list_of_keywords[temp[0]][1]))

#         i+=1

#     return to_return

# def counts(row):


#     return len(row)


# df['Body_processed_topics_words'] = df.apply(lambda x: getTopicsfromKwrds(x['Body_processed_topics']), axis=1)


print(len(df['Body_processed_topics_sorted']))