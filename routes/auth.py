from flask import Blueprint, render_template, request, redirect, url_for, flash, session
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint('auth', __name__)

import sqlite3

def init_db():
    with sqlite3.connect('users.db') as con:
        cur = con.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )''')

        cur.execute('''CREATE TABLE IF NOT EXISTS rooms (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            room_name TEXT UNIQUE NOT NULL
        )''')

        cur.execute('''CREATE TABLE IF NOT EXISTS room_members (
            user_id INTEGER,
            room_id INTEGER,
            FOREIGN KEY(user_id) REFERENCES users(id),
            FOREIGN KEY(room_id) REFERENCES rooms(id)
        )''')

        con.commit()

init_db()


# === Регистрация ===
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password)
        
        try:
            with sqlite3.connect('users.db') as con:
                cur = con.cursor()
                cur.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
                con.commit()
                flash('Регистрация прошла успешно! Войдите в систему.', 'success')
                return redirect(url_for('auth.login'))
        except sqlite3.IntegrityError:
            flash('Имя пользователя уже занято!', 'danger')
    
    return render_template('register.html')

# === Авторизация ===
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        with sqlite3.connect('users.db') as con:
            cur = con.cursor()
            cur.execute("SELECT password FROM users WHERE username = ?", (username,))
            user = cur.fetchone()
        
        if user and check_password_hash(user[0], password):
            session['username'] = username
            flash('Вы успешно вошли!', 'success')
            return redirect(url_for('auth.protected'))
        else:
            flash('Неверное имя пользователя или пароль!', 'danger')
    
    return render_template('login.html')

# === Выход из системы ===
@auth_bp.route('/logout')
def logout():
    session.pop('username', None)
    flash('Вы вышли из системы.', 'success')
    return redirect(url_for('auth.login'))

# === Защищенная страница ===
@auth_bp.route('/protected')
def protected():
    if 'username' not in session:
        flash('Сначала войдите в систему.', 'warning')
        return redirect(url_for('auth.login'))
    return render_template('chat.html', username=session['username'])

# === Домашняя страница ===
@auth_bp.route('/')
def home():
    return redirect(url_for('auth.login'))
