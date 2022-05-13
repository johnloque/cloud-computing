from flask import Flask, request, render_template
import pandas as pd
import numpy as np

app = Flask(__name__)

#db functions

def create_db():
    base_words = ['chien','chat','voiture']
    base_counts = [0] * len(base_words)
    db = []
    for word, count in zip(base_words, base_counts):
        db.append({'words':word, 'counts':count})
    return db

#play functions

def draw_word():
    df = pd.DataFrame(db)
    logits = pd.Series(df['counts'].map(lambda x : df['counts'].max() - x + 1))
    new_word_id = np.random.choice([i for i in range(len(df))], p=logits/sum(logits))
    return new_word_id

def mask_word(target_list, guessed_letters):
    masked_word = ''
    for char in target_list :
        if char in guessed_letters :
            masked_word += char
        else :
            masked_word += '*'
    return masked_word

#global variables

db = create_db()
n_trials = 10
target_list = []
guessed_letters = []
win = False

#endpoints

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/db')
def display_db():
    return render_template('db.html', db=db)

@app.route('/play', methods=['GET','POST'])
def play_hangman():
    global db
    global n_trials
    global target_list
    global guessed_letters
    global win

    if request.method == 'GET':
        new_word_id = draw_word()
        new_word = db[new_word_id]['words']
        db[new_word_id]['counts'] += 1
        n_trials = 10
        target_list = [char for char in new_word]
        guessed_letters = []
        win = False
        masked_word = mask_word(target_list, guessed_letters)
        return render_template('play.html', n_trials = n_trials, new_word=masked_word, field_name='Suggest a new character : ', win=win)

    elif request.method == 'POST':
        new_letter = request.form['guess'].lower()
        if new_letter in guessed_letters :
            masked_word = mask_word(target_list, guessed_letters)
            field_name = "You have already suggested this letter. Suggest another one : "
            return render_template('play.html', n_trials = n_trials, new_word=masked_word, field_name=field_name, win=win)
        else :
            guessed_letters.append(new_letter)
            masked_word = mask_word(target_list, guessed_letters)
            n_trials -= 1
            if all(char in guessed_letters for char in list(set(target_list))) :
                win = True
            return render_template('play.html', n_trials = n_trials, new_word=masked_word, field_name='Suggest a new character : ', win=win)