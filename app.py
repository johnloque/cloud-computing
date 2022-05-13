from flask import Flask, request, render_template
import numpy as np

app = Flask(__name__)

#db functions

def create_db():
    base_words = ['dog','cat','truck','tacos','shoe','computer','student','project']
    base_counts = [0] * len(base_words)
    db = []
    for word, count in zip(base_words, base_counts):
        db.append({'words':word, 'counts':count})
    return db

#play functions

def draw_word():
    counts = [dic["counts"] for dic in db]
    logits = np.array(list(map(lambda x: max(counts) - x + 1, counts)))
    new_word_id = np.random.choice([i for i in range(len(counts))], p=logits/sum(logits))
    return new_word_id

def mask_word(target_list, guessed_letters):
    masked_word = ''
    for char in target_list :
        if char in guessed_letters :
            masked_word += f'{char} '
        else :
            masked_word += '_ '
    return masked_word

#global variables

db = create_db()
n_trials = 10
target_list = []
guessed_letters = []
win = False
history = {'games_played' : 0, 'won' : 0, 'n_trials' : []}

#endpoints

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/db')
def display_db():
    return render_template('db.html', db=db)

@app.route('/db', methods=('GET', 'POST'))
def add_word():
    global db
    list_word = [db[elt]["words"] for elt in range(len(db))]
    if request.method == 'POST': 
        word = request.form['word']
        if word not in list_word:
            db.append({'words':word, 'counts':0})
            field_name = f"The word '{word}' has been added!"
            return render_template('db.html', db =db, field_name=field_name)
        else : 
            field_name = f"The word '{word}' already exists..."
            return render_template('db.html',db=db,field_name=field_name)
    elif request.method == 'GET':
        return render_template('db.html',db=db)

@app.route('/play', methods=['GET','POST'])
def play_hangman():
    global db
    global n_trials
    global target_list
    global guessed_letters
    global win
    global history

    if request.method == 'GET':
        history['games_played'] += 1
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
            if new_letter not in target_list :
                n_trials -= 1
            if all(char in guessed_letters for char in list(set(target_list))) :
                win = True
                history['won'] += 1
                history['n_trials'].append(10-n_trials)
            return render_template('play.html', n_trials = n_trials, new_word=masked_word, field_name='Suggest a new character : ', win=win)

@app.route('/history')
def display_history():
    global history
    while len(history['n_trials']) < history['games_played'] :
        history['n_trials'].append(10)
    history['sum_n_trials'] = sum(history['n_trials'])
    return render_template('history.html', history=history, plot_path = 'history.png')