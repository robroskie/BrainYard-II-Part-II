
#https://goodboychan.github.io/python/datacamp/natural_language_processing/2020/07/17/04-TF-IDF-and-similarity-scores.html

import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

text_file = 'randomPosts.csv'


tfidf_vectorizer = TfidfVectorizer()






df = pd.read_csv('randomPosts.csv', encoding='utf-8')
    # df = df[df['Body'].notna()]

df = df[df['PostTypeId'] == 1]

df.head()


indices = pd.Series(df.index, index=df['Body']).drop_duplicates()

def get_recommendations(Body, cosine_sim, indices):
    # Get the index of the movie that matches the title
    idx = indices[Body]
    # Get the pairwsie similarity scores
    sim_scores = list(enumerate(cosine_sim[idx]))
    # Sort the movies based on the similarity scores
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    # Get the scores for 10 most similar movies
    sim_scores = sim_scores[1:11]
    # Get the movie indices
    movie_indices = [i[0] for i in sim_scores]
    # Return the top 10 most similar movies
    return df['Body'].iloc[movie_indices]









text = 'ould like to know how i can initialize an array(or list), yet to be populated with values, to have a defined size'


def cSim(text):



    print(df)

    comments = df['Body']

    tfidf = TfidfVectorizer(stop_words='english')

    # Construct the TF-IDF matrix
    tfidf_matrix = tfidf.fit_transform(comments)

    # Generate the cosine similarity matrix
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

   
    # Generate recommendations
    print(get_recommendations(text, cosine_sim, indices))




cSim(text)

print(a)