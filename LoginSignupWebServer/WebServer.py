from flask import Flask, render_template, redirect, url_for, request
import sqlite3

app = Flask(__name__)

def validate(username, password):
    completion = False
    with sqlite3.connect('static/db.db') as con:        #il with asseggna temporaneamente un valore ad una variabile
        #con = sqlite3.connect('static/db.db')           una volta finito il blocco l'assegnazione non vale più (al return)
                cur = con.cursor()
                cur.execute("SELECT * FROM USERS")
                rows = cur.fetchall()
                for row in rows:
                    dbUser = row[0]     #row = lista di tuple, ogni tupla ha 2 celle -> la prima contiene lo user, la seconda la pwd
                    dbPass = row[1]
                    if dbUser==username:
                        completion = check_password(dbPass, password)
    return completion

def check_password(hashed_password, user_password):
    return hashed_password == user_password

def register(user, pwd):
    loaded = False

    with sqlite3.connect('static/db.db') as con:
        cur = con.cursor()
        cur.execute(f'INSERT INTO USERS ("USERNAME", "PASSWORD") VALUES ("{user}", "{pwd}")')
        loaded = True
        
    return loaded

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        loaded = register(username, password)
        if loaded == False:
            error = 'This username already exists, please choose another one!'
        else:
            
            return redirect(url_for('toconfirm'))
    return render_template('signup.html', error=error)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        completion = validate(username, password)
        if completion == False:
            error = 'Invalid Credentials. Please try again.'
        else:
            return redirect(url_for('secret'))
    return render_template('login.html', error=error) 

@app.route('/', methods=['GET', 'POST'])
def home():
    error = None
    if request.method == 'POST':
        if request.form['choice_btn'] == "Login":
            return redirect(url_for('login'))
        if request.form['choice_btn'] == "Signup":
            return redirect(url_for('signup'))
    return render_template('home.html', error=error)

@app.route('/toconfirm')
def toconfirm():
    return "Please check your e-mail and click on the link to activate your account!"

@app.route('/secret')
def secret():
    return "This is a secret page!"

if __name__== "__main__":
    app.run()