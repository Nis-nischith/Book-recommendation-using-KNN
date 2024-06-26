
# import libraries (you may add additional imports but you may not have to)
import numpy as np
import pandas as pd
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors
import matplotlib.pyplot as plt
from scipy.sparse import csr_matrix

# get data files
!wget https://cdn.freecodecamp.org/project-data/books/book-crossings.zip

!unzip book-crossings.zip

books_filename = 'BX-Books.csv'
ratings_filename = 'BX-Book-Ratings.csv'

# import csv data into dataframes
df_books = pd.read_csv(
    books_filename,
    encoding = "ISO-8859-1",
    sep=";",
    header=0,
    names=['isbn', 'title', 'author'],
    usecols=['isbn', 'title', 'author'],
    dtype={'isbn': 'str', 'title': 'str', 'author': 'str'})

df_ratings = pd.read_csv(
    ratings_filename,
    encoding = "ISO-8859-1",
    sep=";",
    header=0,
    names=['user', 'isbn', 'rating'],
    usecols=['user', 'isbn', 'rating'],
    dtype={'user': 'int32', 'isbn': 'str', 'rating': 'float32'})

df_books = df_books.drop('author', axis=1)
df_books.info()

df_books.head()

counts= df_ratings['user'].value_counts()
ratings = df_ratings[df_ratings['user'].isin(counts[counts>100].index)]

ratings.info()

ratings

merge_data = pd.merge(df_books, ratings, on='isbn').drop('isbn', axis=1)
merge_data

merge_data= merge_data.drop_duplicates({'title', 'user'})
data_pivot= merge_data.pivot(index='title', columns='user', values='rating').fillna(0)
data_matrix = csr_matrix(data_pivot.values)

data_pivot

data_matrix

model = NearestNeighbors(metric='cosine', algorithm='brute', p=2)
model.fit(data_matrix)

# function to return recommended books - this will be tested
def get_recommends(n=6):
  recommended_books = []
  query_index = np.random.choice(data_pivot.shape[0])
  distances, indices = model.kneighbors(data_pivot.iloc[query_index,:].values.reshape(1, -1), n_neighbors = n)
  for i in indices:
    recommended_books.append(data_pivot.index[i])
  return recommended_books, distances

recommended_books, distances = get_recommends(6)

for i in recommended_books:
  print(i)

for i in distances:
  print(i)
