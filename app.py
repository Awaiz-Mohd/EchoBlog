from flask import Flask, render_template, request, redirect, url_for, session
import subprocess
import threading
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key' 

streamlit_process = None

def init_db():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users 
                      (id INTEGER PRIMARY KEY, username TEXT UNIQUE, password TEXT)''')
    conn.commit()
    conn.close()

def run_streamlit():
    """Function to run the Streamlit app."""
    global streamlit_process
    streamlit_process = subprocess.Popen(["streamlit", "run", "main.py"])  # Replace 'main.py' with your Streamlit file name

@app.route('/')
def home():
    return redirect(url_for('index'))
@app.route('/index')
def index():
    return render_template('index.html')
@app.route('/login', methods=['GET', 'POST'])
def login():
    global streamlit_process
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute("SELECT password FROM users WHERE username=?", (username,))
        user = cursor.fetchone()
        conn.close()
        
        if user and check_password_hash(user[0], password): 
            session['username'] = username 
            
            if streamlit_process is None or streamlit_process.poll() is not None:
                threading.Thread(target=run_streamlit).start()  
            
            return redirect(url_for('home'))  
        else:
            return render_template('login.html', error='Invalid username or password.')

    return render_template('login.html')  

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password) 
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", 
                           (username, hashed_password))
            conn.commit()
            return redirect(url_for('login'))  
        except sqlite3.IntegrityError:
            return render_template('register.html', error='Username already exists.')
        finally:
            conn.close()

    return render_template('register.html')  
@app.route('/logout')
def logout():
    global streamlit_process
    session.pop('username', None) 

    if streamlit_process is not None:
        streamlit_process.terminate()  
        streamlit_process = None  

    return redirect(url_for('login'))  


@app.route('/logout', endpoint='user_logout') 
def logout():
    global streamlit_process
    session.pop('username', None) 

    
    if streamlit_process is not None:
        streamlit_process.terminate()  
        streamlit_process = None  

    return redirect(url_for('login'))  
if __name__ == '__main__':
    init_db()  
    app.run(debug=True)
