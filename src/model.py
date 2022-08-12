import tensorflow as tf
import keras
from keras.models import Sequential
from keras.layers.core import Dense
import pandas as pd

training_data = pd.read_csv('data/mySpotify.csv')

features = ['danceability', 'energy', 'loudness', 'speechiness', 'acousticness',
            'instrumentalness', 'valence', 'tempo']

x_train = training_data[features]
y_train = training_data['target']

model = Sequential()
model.add(Dense(12, input_shape=(8,), activation='relu'))
model.add(Dense(8, activation='relu'))
model.add(Dense(1, activation='sigmoid'))

model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

model.fit(x_train, y_train, epochs=150, batch_size=10)

_, accuracy = model.evaluate(x_train, y_train)

predictor = pd.read_csv('data/searchSpotify2.csv')
predictions = model.predict(predictor[features])

liked_ids = []
i = 0


for prediction in predictions:
    if(prediction==1):
        liked_id = predictor.loc[i]['id']
        print(liked_id)
        liked_ids = liked_id
        i += 1

print(i)

# print(liked)
