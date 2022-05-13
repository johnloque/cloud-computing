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

db = create_db()

#play functions

def draw_word():
    df = pd.DataFrame(db)
    logits = pd.Series(df['counts'].map(lambda x : df['counts'].max() - x + 1))
    new_word_id = np.random.choice([i for i in range(len(df))], p=logits/sum(logits))
    return new_word_id

n_trials = 10

#endpoints

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/db')
def display_db():
    return render_template('db.html', db=db)

@app.route('/play', methods=['GET','POST'])
def display_word():
    global n_trials
    if request.method == 'GET':
        new_word_id = draw_word()
        new_word = db[new_word_id]['words']
        return render_template('play.html', n_trials = n_trials, new_word=new_word)
    elif request.method == 'POST':
        text = request.form['guess'].lower()
        n_trials -= 1
        return render_template('play.html', n_trials = n_trials, new_word=text)