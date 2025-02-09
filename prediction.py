import pandas as pd
import joblib

## input MUST be a formatted file, use formattingInput.py
def predict_and_update_metadata(formatted_file, original_file, output_file):
    rf = joblib.load('random_forest_model.pk1')
    mlb = joblib.load('multi_label_binarizer.pk1')

    formatted_data = pd.read_csv(formatted_file)

    df_original = pd.read_csv(original_file)

    ## X_new is different from X since X is found in the modelTraining
    X_new = formatted_data[['energy_%', 'bpm', 'danceability_%', 'liveness_%', 'valence_%', 
                 'speechiness_%', 'instrumentalness_%']]
    
    predicted = rf.predict(X_new)

    ## inverse_transform changes the data from binary back to readable text
    emotion_tags = mlb.inverse_transform(predicted)

    ## now we sets the tags column of formatted_data to this tags value and we format it correctly
    formatted_data['tags'] = ['[' + ', '.join(tags) + ']' for tags in emotion_tags]

    df_result = pd.concat([df_original[['track_artist', 'playlist_genre', 'track_name', 'track_album_name']], formatted_data['tags']], axis=1)

    df_result.to_csv(output_file, index=False)

formatted_file = 'add_tags_formatted.csv'
original_file = 'add_tags_data.csv'
output_file = 'add_tags_data_with_tags.csv'
predict_and_update_metadata(formatted_file, original_file, output_file)