import joblib
clf = joblib.load("Mood_MLP.pkl")

#importing packages

#using this for CSV file reading and writing
import pandas as pd

#using a generic MLP classifier
from sklearn.neural_network import MLPClassifier

#using this to split the dataset up
from sklearn.model_selection import train_test_split

#using this to perform some validation.
from sklearn.model_selection import cross_val_score

#using this so we can standardize our data
from sklearn.preprocessing import StandardScaler
import sklearn
import numpy as np

#this is the header of the input data
names2 = ['duration', 'danceability', 'energy', 'loudness', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo', 'URI']

#file path of the input data
url2 = '/Resources/clean_data.csv'

#reading the dataset into a pandas dataframe
dataset2 = pd.read_csv(url2, names=names2)

#separating the input from the song URI
dataToMakePredictionsOn = dataset2.values[:,0:10]

#we are using the standard scaler to scale the data
scaler = StandardScaler()

#standardizing the data
X_std2 = scaler.fit_transform(dataToMakePredictionsOn)

#making predictions on the input data
predictions = clf.predict(X_std2)

#turning the standardized dataset into a dataframe
X_std2 = pd.DataFrame(X_std2, columns = ['duration', 'danceability', 'energy', 'loudness', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo'])

#inserting the mood predictions into the original datasets dataframe
dataset2.insert(10, "Mood", predictions, True)

#taking the predictions and standardizing them
standardizedPredictions = scaler.fit_transform(predictions.reshape(-1, 1))

#inserting the mood predictions into the standardized dataset so we can use this later
X_std2.insert(10, "Mood", standardizedPredictions, True)

#now that we have the data clustered, we must get recommended songs

#to do this, we have to find the n closest songs/points to the input.

#we can kind of cheat this and use kNN

X_std2 = pd.DataFrame(X_std2)
X_std2 = X_std2.values
from sklearn.neighbors import NearestNeighbors
nums = input("enter the number of songs you want \n")
knn = NearestNeighbors(n_neighbors=int(nums))
knn.fit(X_std2)


print(NearestNeighbors(algorithm='auto', leaf_size=500, metric = 'cosine'))

#replace knn.kneighbors(X_std2[1].reshape(1, -1) with input value
recommendations = knn.kneighbors(X_std2[1].reshape(1, -1), return_distance=False)


#once we have the values, we just have to search the dataset for the spotify
#URI, then we can use the URI to get the song name
for val in recommendations:
  print(dataset2.iloc[val]['URI'], '\n')




