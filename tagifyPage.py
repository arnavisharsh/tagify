import streamlit as st
import pandas as pd

# Load the CSV file with individual tag columns
df = pd.read_csv('add_tags_data_with_individual_tags.csv')

# Set up Streamlit page configuration
st.set_page_config(page_title="TAGIFY", layout="wide")

# Title of the app
st.title("🎶 TAGIFY 'Tag your music!'")

# Emotion color mapping
emotion_colors = {
    "Angry": "red",
    "Happy": "green",
    "Sad": "blue",
    "Energetic": "orange"
}

# Define a function to filter songs by clicked tag
def filter_by_tag(tag):
    # Filter songs that have the selected tag in any of the tag columns
    filtered_df = df[(df['tag_1'] == tag) | (df['tag_2'] == tag) | (df['tag_3'] == tag)]
    return filtered_df.drop_duplicates(subset=['track_name', 'track_artist', 'track_album_name'])

# Function to display songs and allow adding to playlist
def display_songs(playlist):
    st.write("Click on any tag to filter songs by that emotion:")

    # Search bar
    search_query = st.text_input("Search Songs", "")

    # Filter the dataframe based on the search query (if any)
    if search_query:
        df_filtered = df[df['track_name'].str.contains(search_query, case=False) | df['track_artist'].str.contains(search_query, case=False)]
    else:
        df_filtered = df

    # Remove duplicates based on track name, artist, and album
    df_filtered = df_filtered.drop_duplicates(subset=['track_name', 'track_artist', 'track_album_name'])

    # Dictionary to keep track of tag display toggles
    if "tag_display" not in st.session_state:
        st.session_state.tag_display = {}

    # Display each song with its tags and provide buttons for filtering
    for index, row in df_filtered.iterrows():
        song_tags = [row['tag_1'], row['tag_2'], row['tag_3']]  # Get the tags for this song
        song_name = row['track_name']
        artist = row['track_artist']
        album = row['track_album_name']

        # Filter the tags to only include emotion tags
        filtered_tags = [tag for tag in song_tags if tag in emotion_colors]

        # Display song name with tags inline, and artist and album on the next line
        tag_buttons = []
        for tag in song_tags:
            if tag in emotion_colors:
                tag_buttons.append(f'<button style="background-color: {emotion_colors[tag]}; font-size: 12px; margin: 2px; padding: 5px; border-radius: 3px;">{tag}</button>')
            else:
                tag_buttons.append(f'<button style="background-color: gray; font-size: 12px; margin: 2px; padding: 5px; border-radius: 3px;">{tag}</button>')

        # Display song title and tags inline
        st.markdown(f"<div style='display: flex; align-items: center;'><h3 style='margin: 0;'>{song_name} </h3>" + " ".join(tag_buttons) + "</div>", unsafe_allow_html=True)
        st.markdown(f"**Artist:** {artist} | **Album:** {album}")

        # Show the tags as buttons and allow users to filter by clicking on them
        for tag in song_tags:
            tag_key = f"{index}_{tag}"
            if tag_key not in st.session_state.tag_display:
                st.session_state.tag_display[tag_key] = False

            if st.button(tag, key=tag_key):
                st.session_state.tag_display[tag_key] = not st.session_state.tag_display[tag_key]

            if st.session_state.tag_display[tag_key]:
                filtered_df = filter_by_tag(tag)
                st.write(f"Found {filtered_df.shape[0]} songs with the tag {tag}.")
                st.dataframe(filtered_df)

        # Add or Remove song from playlist
        add_remove_button_key = f"add_remove_{index}_{song_name}_{artist}_{album}"
        if song_name in playlist:
            if st.button(f"➖ Remove {song_name} from Playlist", key=add_remove_button_key):
                playlist.remove(song_name)
                st.write(f"{song_name} removed from your playlist.")
        else:
            # Show a "+" button to add the song to the playlist
            add_to_playlist_button = st.button(f"➕ Add {song_name} to Playlist", key=add_remove_button_key)
            if add_to_playlist_button:
                # Prompt user to select a playlist to add to
                if "playlists" in st.session_state and len(st.session_state.playlists) > 0:
                    selected_playlist = st.selectbox("Select a Playlist", list(st.session_state.playlists.keys()))
                    if selected_playlist:
                        if song_name not in st.session_state.playlists[selected_playlist]:
                            st.session_state.playlists[selected_playlist].append(song_name)
                            st.write(f"{song_name} added to {selected_playlist} playlist.")
                        else:
                            st.write(f"{song_name} is already in the {selected_playlist} playlist.")
                else:
                    st.write("You need to create a playlist first.")

    return playlist

# Function to display playlists
def display_playlists():
    if "playlists" not in st.session_state:
        st.session_state.playlists = {}

    # Create a new playlist
    playlist_name = st.text_input("Create a new playlist", "")
    if playlist_name:
        if playlist_name not in st.session_state.playlists:
            st.session_state.playlists[playlist_name] = []

    # Display existing playlists with clickable headers
    st.write("Click a playlist to view its songs:")
    for playlist_name in st.session_state.playlists:
        if st.button(f"🎵 {playlist_name}", key=f"view_{playlist_name}"):
            if "current_playlist" in st.session_state and st.session_state.current_playlist == playlist_name:
                st.session_state.current_playlist = None  # Close the playlist view
            else:
                st.session_state.current_playlist = playlist_name  # Open the playlist view

        if "current_playlist" in st.session_state and st.session_state.current_playlist == playlist_name:
            display_playlist_songs(playlist_name)

# Function to display the songs in a selected playlist
def display_playlist_songs(playlist_name):
    if playlist_name in st.session_state.playlists:
        playlist = st.session_state.playlists[playlist_name]
        if not playlist:
            st.write("This playlist is empty. Add songs to it from the Song Library.")
        else:
            # Display the playlist name as a subheader
            st.subheader(f"{playlist_name} Playlist")

            # Display each song in the playlist with a "-" button in front of the song name
            for song in playlist:
                song_details = df[df['track_name'] == song]
                for index, row in song_details.iterrows():
                    song_name = row['track_name']
                    artist = row['track_artist']
                    album = row['track_album_name']
                    song_tags = [row['tag_1'], row['tag_2'], row['tag_3']]
                    filtered_tags = [tag for tag in song_tags if tag in emotion_colors]

                    # Display song with tags and remove button inline
                    col1, col2 = st.columns([1, 9])
                    with col1:
                        if st.button("➖", key=f"remove_{song_name}_{artist}_{album}"):
                            st.session_state.playlists[playlist_name].remove(song_name)
                            st.write(f"{song_name} removed from {playlist_name}.")
                    with col2:
                        tag_buttons = []
                        for tag in song_tags:
                            if tag in emotion_colors:
                                tag_buttons.append(f'<button style="background-color: {emotion_colors[tag]}; font-size: 10px; margin: 2px; padding: 4px; border-radius: 3px;">{tag}</button>')
                            else:
                                tag_buttons.append(f'<button style="background-color: gray; font-size: 10px; margin: 2px; padding: 4px; border-radius: 3px;">{tag}</button>')

                        st.markdown(f"<div style='display: flex; align-items: center;'><h3 style='margin: 0;'>{song_name} </h3>" + " ".join(tag_buttons) + "</div>", unsafe_allow_html=True)
                        st.markdown(f"**Artist:** {artist} | **Album:** {album}")

# Main app structure: Navigation through pages
menu = ["Home", "Song Library", "My Playlist"]
choice = st.sidebar.radio("Select Page", menu)

# Initialize playlist as an empty list in session state
if "playlist" not in st.session_state:
    st.session_state.playlist = []

if choice == "Home":
    st.write("Welcome to TAGIFY! Use the navigation on the left to browse songs, create playlists, and more.")
    st.write("Copyright soon ... jk this is still in the beta stages :( ")
    st.write("Enjoy our dataset of songs tagged by its emotion/vibe!")
    st.write("Click on each emotion to see the sets of songs with the same emotion!")
    st.write("Use the sidebar to explore the Song Library or My Playlist.")
    st.write("This program was trained on a Random Forest Classifier and learns what type of emotion different songs are based on the songs sound characteristics. This program breaks down into the following emotions:")
    for emotion, color in emotion_colors.items():
        st.markdown(
            f"""
            <div style='background-color: {color}; padding: 10px; margin: 5px; border-radius: 5px;'>
                <h4 style='color: white;'>{emotion}</h4>
            </div>
            """,
            unsafe_allow_html=True
        )
elif choice == "Song Library":
    st.subheader("🎶 Song Library")
    st.session_state.playlist = display_songs(st.session_state.playlist)  # Display songs and allow adding/removing from playlist
elif choice == "My Playlist":
    st.subheader("🎶 My Playlist 🎶")
    display_playlists()  # Show the