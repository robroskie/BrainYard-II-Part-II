

#https://goodboychan.github.io/python/datacamp/natural_language_processing/2020/07/17/04-TF-IDF-and-similarity-scores.html

import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def getCSim(text):

    text_file = 'randomPosts.csv'


    tfidf_vectorizer = TfidfVectorizer()


    df = pd.read_csv('randomPosts.csv', encoding='utf-8')
    df = df[df['Body'].notna()]

    df = df[df['PostTypeId'] == 1]

    # df.reset_index(drop=True, inplace=True)

    df.head()

    # text = 'ould like to know how i can initialize an array(or list), yet to be populated with values, to have a defined size'

    df_input = pd.DataFrame({'Body' : [text]})

    df_results = pd.DataFrame()

    toAdd = {'Body' : text}


    df_input = df_input.append([toAdd]*21401)

    question = df_input['Body']
    comments = df['Body']

    vectorizer = TfidfVectorizer()



    # VVVVVVVVVVVVVVVVVVVVVVVV


    # for i in range(1, 21402):
    #     vectors = vectorizer.fit_transform([text, comments[i]])
    #     feature_names = vectorizer.get_feature_names_out()
    #     dense = vectors.todense()
    #     denselist = dense.tolist()
    #     dfcs = pd.DataFrame(denselist, columns=feature_names)

    #     cosine_sim = cosine_similarity(dfcs, dfcs)
    #     df_results = df_results.append({'postID' : df.index[i], 'Csim_Score' : cosine_sim[0][1]}, ignore_index = True)




    # df_results = df_results[df_results['Csim_Score'].notna()]
    # df_results = df_results.sort_values('Csim_Score', ascending=False)

    # df_results_top10 = df_results.head(10)


    # ^^^^^^^^^^^^^^^^^^^^^^^^^



    # df_results.to_csv('cosSimMatches.csv', encoding='utf-8')

    # df.to_csv('postsToLookup.csv', encoding='utf-8')


    df_results_top10 = pd.read_csv('cosSimMatches.csv', encoding='utf-8')


    print(df_results_top10.head(10))



    df_final = df.merge(df_results_top10, how='outer', left_index=True, right_index=True)

    df_final = df_final.head(10)

    print(df_final.head(10)['Body'])


    print(str(df_final['Body']))

    to_return = list(df_final['Body'])
    



    for e in to_return:
        print(e)
        print('************')


    to_return 



getCSim('would like to know how i can initialize an array(or list), yet to be populated with values, to have a defined size')