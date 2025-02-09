# tagify #

ML project that tags songs with emotions/vibes.

________________________________________________________________________________________

Arnav Harsh - Single collaborator, first ever hackathon project :)

________________________________________________________________________________________

This project was created for my passion for music.

The biggest issue I face with current day music streaming services is the ability to filter a playlist.

Most of the playlists I have are worth 20 GB and consist of over 4000 songs! Crazy right!

The biggest issues with these playlists was being able to pick the vibe I wanted in the current moment.

What I wanted to do is create some music app that can determine what emotion/vibe each song had so you can easily filter
and pick songs of a certain vibe you are looking for.

Currently the model was only trained for a select few emotions: Happy, Angry, Sad, Energetic ...

________________________________________________________________________________________

I utilized a variety of tools including, VS CODE to program, CHATGPT and COPILOT to help debug, as well as a plethora of API's (detailed in the following block).

________________________________________________________________________________________

The API's I used include:
- Pandas -> HEAVILY used for the datasets and CSV files.
- Sylearn  -> used to train the Random Forest Classifier ML model, also used to convert the tags into binary numbers.
- Ast -> used to help fix discrepences with the way the tags were saved.
- joblib -> used to basically import the ML trained model to another file to be able to run the trained code.
- streamlit -> used for the UI and the front end.
- Kaggle -> downloaded all datasets used for this project through kaggle.

________________________________________________________________________________________

Some of the major challenges I faced in this project was the ability to have clean, organized data that can be processed easily.

There were multiple instances where I had cleaned the CSV files partially but somehow managed to mess something up which led to issues down the line.

This was a huge issue when it came to UI since the 'tags' saved by the ML model were put in a list and that list was saved as a string.

This led to issues accessing this data and being able to process it.

The solution was hours of debugging and ultimately saving each tag in a different column to avoid these issues.

________________________________________________________________________________________
