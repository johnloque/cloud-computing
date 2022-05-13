# Cloud Computing
This repository contains the assessment for Antoine Chancel's Cloud Computing course (ENSAE Paris, 2022).

## Project Details
Regarding our assessment, the main objective was to develop an application with Flask. The creation of this API had to be joined to its implementation in dockers. 

We decided to developp a Hangman API.

## Content
The hangman API is divided into 4 different web pages :
- The 'home' page, where the user has the possibility to start a new game or to add a new word to the existing database.
- The 'play' page, which contains the main part of our application. This page will allow the user to play Hangman, by suggesting letters. In return, the application will let the user know if his suggested letter is present in the word to guess or not, and if it is the case, it will reveal this letter of the hidden word.
- The 'database' page, which will allow the user to consult the words already present in the current database, but also to add other words in order to enrich it.
- The 'history' page, which will allow the user to be aware of the number of wins or loses he has on his record.

## Files
The files in this repository should be (at least) :
- README.md
- Dockerfile
- app.py
- templates
    - index.html
    - play.html
    - db.html
    - history.html
- requirements.txt
- .gitignore

## Students
The students involved in this project are :
- BAHI Prisca
- CAPOT Michel
- CHEKEMBOU Dounia
- TAWFIKI Réda
- VERDIÈRE Jeffrey