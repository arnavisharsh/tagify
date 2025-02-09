import pandas as pd

def format_csv(input_file, output_file):

    target_columns = ['energy_%', 'bpm', 'danceability_%', 'liveness_%', 'valence_%', 
                 'speechiness_%', 'instrumentalness_%']
    
    df = pd.read_csv(input_file)

    column_map = {
        'energy': 'energy_%',  # energy to energy_%
        'bpm': 'bpm',
        'tempo' : 'bpm',
        'danceability': 'danceability_%',
        'liveness': 'liveness_%',
        'valence': 'valence_%',
        'speechiness': 'speechiness_%',
        'instrumentalness': 'instrumentalness_%',
    }

    df.columns= [column_map.get(col, col) for col in df.columns]

    df = df[target_columns]

    df.to_csv(output_file, index=False)

format_csv('add_tags_data.csv', 'add_tags_data_with_tags.csv')