import sklearn
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score
from sklearn.preprocessing import LabelEncoder
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import precision_recall_fscore_support
from sklearn.neighbors import NearestNeighbors
import numpy as np
import pandas as pd
import joblib
import random

def dataFix():
  #Loading the model we previously trained
  clf = joblib.load("models/Mood_MLP.pkl")


  """Normalizing the Data"""

  #Gives pandas the location of the dataset file
  filePath = "Resources/spotify_data.csv"
  #putting the dataset file into a pandas dataframe
  spotify_data = pd.read_csv(filePath)



  headers = ['popularity', 'danceability', 'energy', 'key', 'loudness', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo', 'duration_ms']

  dataToBeNormalized = spotify_data[headers]

  scaler = StandardScaler()

  scaler.fit(dataToBeNormalized)

  normalizedData = pd.DataFrame(scaler.transform(dataToBeNormalized), columns = headers)

  for header in headers:
    spotify_data[header] = normalizedData[header]



  """Getting the Mood Feature"""

  #we have already used the master dataset earlier, as well as normalized it
  #, so we can get data from it.
  dataToMakePredictionsOn = spotify_data[['duration_ms', 'danceability', 'energy', 'loudness', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo']]

  #storing the mood dataset
  masterDatasetMood = clf.predict(dataToMakePredictionsOn)
  spotify_data['mood'] = masterDatasetMood

  spotify_data['track_name'] = spotify_data['track_name'].str.lower()
  spotify_data['artist_name'] = spotify_data['artist_name'].str.lower()

  songDatabase = spotify_data.to_numpy()

  #getting the genre column from the dataset
  genre = spotify_data['genre']

  #changing this genre column to a numpy array to be used with the label encoder
  genre = np.array(genre)

  #instantiating the label encoder
  encoder = sklearn.preprocessing.LabelEncoder()

  #getting the genre classes
  encoder.fit(genre.reshape(-1, 1))

  #changing the genre column to reflect the label encoding
  genre = encoder.transform(genre.reshape(-1, 1))

  #turning the genre array back into a dataframe
  genre = pd.DataFrame(genre)

  #replacing the genre column in the dataset with genre
  spotify_data['genre'] = genre

  #getting the values of the features within the dataset. 
  features = spotify_data.values[:,4:20]

  return [spotify_data, songDatabase, features]


"""Taking inputs to find the recommended songs"""

def recommendSongs(playlist, sizeOfNewPlaylist):
    
    #Creating a set of all the users songs inputted
    playlistSet = set(song for song in playlist)
    
    #This function must be called to add Mood to dataset and normalize the data for every model we make 
    spotify_data, songDatabase, features = dataFix()
  
    recommendations = []
    #getting the index of the song
    
    for i, song in enumerate(playlist):
      print("\nsong", song, i)
      try:
        #getting the index of the matching spotify URI from the dataset
        URIIndex = spotify_data.index[spotify_data['track_id'] == playlist[i]].tolist()
        
        #setting the number of song recommendations to get
        knn = NearestNeighbors(algorithm='auto', leaf_size=500, metric = 'cosine', n_neighbors = 7)
        
        #fitting the features of the dataset using the kNN algorithm
        knn.fit(features)
  
        #getting the values and adding them to the recommendations list. 
        recommendations += knn.kneighbors(features[URIIndex].reshape(1, -1), return_distance=False).tolist()
  
      except ValueError as e:
        print(f"Caught a ValueError: {e}")
  
  
    print("\n\n\nRECOMMENDATIONS**********************************")
    for x in recommendations:
      print("Recommend: ", x)
    
    #Turning the 2D array into 1D
    recommendations = [element for sublist in recommendations for element in sublist]
    
    #Will contain song results with each index including [name, title]
    result = []
    
    resultCount = 0

    #While results doesnt contain the amount of songs the user wanted 
    while resultCount != int(sizeOfNewPlaylist):
        
        i = random.randint(0, len(recommendations) - 1)

        #If recommended song is not in user playlist or in results 
        if songDatabase[recommendations[i]][3] not in playlistSet:
            
            result.append([songDatabase[recommendations[i]][2], songDatabase[recommendations[i]][1]])

            playlistSet.add(songDatabase[recommendations[i]][3])

            resultCount += 1
    
    print("\n\n\nRESULT**********************************")
    for x in result:
      print("Song: ", x)

    return result
