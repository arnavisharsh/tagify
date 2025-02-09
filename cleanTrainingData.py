import pandas as pd
from sklearn.preprocessing import MinMaxScaler, LabelEncoder

spotifyData = pd.read_csv('training_data.csv', encoding='ISO-8859-1')

## makes the % into actual perents
spotifyData['danceability_%'] = spotifyData['danceability_%'].astype(float) / 100
spotifyData['valence_%'] = spotifyData['valence_%'].astype(float) / 100
spotifyData['energy_%'] = spotifyData['energy_%'].astype(float) / 100
spotifyData['acousticness_%'] = spotifyData['acousticness_%'].astype(float) / 100
spotifyData['instrumentalness_%'] = spotifyData['instrumentalness_%'].astype(float) / 100
spotifyData['liveness_%'] = spotifyData['liveness_%'].astype(float) / 100
spotifyData['speechiness_%'] = spotifyData['speechiness_%'].astype(float) / 100

def assign_multiple_tags(row):
    tags = []

    # First, prioritize the strongest emotions (exclusive conditions to avoid conflicts)
    if row['valence_%'] > 0.7 and row['energy_%'] > 0.6:
        tags.append('Happy')  # High valence and energy = Happy
    elif row['valence_%'] < 0.3 and row['energy_%'] > 0.6:
        tags.append('Angry')  # Low valence, high energy = Angry
    elif row['valence_%'] < 0.3 and row['energy_%'] < 0.3:
        tags.append('Sad')  # Low valence and low energy = Sad
    
    # Next, check for more specific but not overlapping emotions
    if row['energy_%'] > 0.6 and row['danceability_%'] > 0.6:
        tags.append('Energetic')  # High energy and danceability = Energetic
    elif row['energy_%'] < 0.3 and (row['liveness_%'] < 0.3 or row['danceability_%'] < 0.4):
        tags.append('Chill')  # Low energy, low danceability, or liveness = Chill
    elif row['energy_%'] < 0.3 and 0.4 < row['valence_%'] < 0.7:
        tags.append('Calm')  # Low energy, moderate valence = Calm
    elif row['energy_%'] > 0.7 and row['danceability_%'] < 0.4:
        tags.append('Excited')  # High energy, low danceability = Excited
    elif row['valence_%'] < 0.4 and row['energy_%'] < 0.6 and row['danceability_%'] < 0.5:
        tags.append('Melancholic')  # Low valence, energy, and danceability = Melancholic

    # Add more specific but non-overlapping emotions
    if row['energy_%'] < 0.3 and row['liveness_%'] > 0.7:
        tags.append('Mellow')  # Low energy, high liveness (live music vibe) = Mellow
    if row['energy_%'] < 0.3 and row['danceability_%'] < 0.4:
        tags.append('Serene')  # Low energy, low danceability = Serene
    if row['energy_%'] < 0.5 and row['valence_%'] > 0.5:
        tags.append('Peaceful')  # Low energy, higher valence = Peaceful

    # Remove duplicates: only keep unique tags
    tags = list(set(tags))

    # Ensure we have exactly 3 distinct tags
    if len(tags) < 3:
        # Add additional tags to ensure 3 distinct emotions
        if 'Happy' not in tags:
            tags.append('Happy')
        if 'Sad' not in tags and len(tags) < 3:
            tags.append('Sad')
        if 'Angry' not in tags and len(tags) < 3:
            tags.append('Angry')
        if 'Energetic' not in tags and len(tags) < 3:
            tags.append('Energetic')
        if 'Chill' not in tags and len(tags) < 3:
            tags.append('Chill')
        if 'Calm' not in tags and len(tags) < 3:
            tags.append('Calm')
        if 'Excited' not in tags and len(tags) < 3:
            tags.append('Excited')
        if 'Melancholic' not in tags and len(tags) < 3:
            tags.append('Melancholic')
        if 'Mellow' not in tags and len(tags) < 3:
            tags.append('Mellow')
        if 'Serene' not in tags and len(tags) < 3:
            tags.append('Serene')
        if 'Peaceful' not in tags and len(tags) < 3:
            tags.append('Peaceful')

    return tags

spotifyData['tags'] = spotifyData.apply(assign_multiple_tags, axis=1)

# Save or display the updated DataFrame
spotifyData.to_csv('training_data_with_tags.csv', index=False)
print(spotifyData)