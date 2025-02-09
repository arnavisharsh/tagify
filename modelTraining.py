import pandas as pd
import joblib as jl
import ast
from  sklearn.model_selection import train_test_split
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.ensemble import RandomForestClassifier

spotifyData = pd.read_csv('training_data_with_tags.csv', encoding='utf-8')

# Remove irrelevant columns from the input data
numeric_columns = ['streams', 'in_deezer_playlists', 'in_shazam_charts']

spotifyData = spotifyData.drop(columns=numeric_columns, errors='ignore')
spotifyData = spotifyData.drop(columns=['mode', 'key'], errors='ignore')

## clean the tag values
spotifyData['tags'] = spotifyData['tags'].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else x)

## set up X valyes, dropping certain values that arent required for the training
# input required values:
# [['energy_%', 'bpm/tempo', 'Danceability', 'Loudness (optional)', 'Liveness', 'Valence', 'Speechiness', 'Instrumentalness']]
# OPTIONAL IMPLEMENTATION: major/key -> would need to first get the key then set it then clean this data

X = spotifyData[['energy_%', 'bpm', 'danceability_%', 'liveness_%', 'valence_%', 
                 'speechiness_%', 'instrumentalness_%']]  # Adjust based on your available columns


## convert the tags to binary numbers for each tag
mlb = MultiLabelBinarizer()
y = mlb.fit_transform(spotifyData['tags'])


## split the group into 80 train and 20 test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=28)


## start creating RandomForestClassifier
## this will train _________________________
rf = RandomForestClassifier(n_estimators=1000,
                            criterion='entropy',
                            min_samples_split=10,
                            max_depth=14,
                            random_state=42) # helps balance the class weights


rf.fit(X_train, y_train)

y_pred = rf.predict(X_test)

jl.dump(rf, 'random_forest_model.pk1')
jl.dump(mlb, 'multi_label_binarizer.pk1')