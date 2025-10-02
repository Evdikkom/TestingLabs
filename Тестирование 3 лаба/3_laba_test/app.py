from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Секретный ключ для сессий

# Простая база данных пользователей (в реальном приложении используйте настоящую БД)
users = {
    "testuser": {
        "password": "testpass",
        "name": "Тестовый Пользователь"
    },
    "a.r.evdokimov": {
        "password": "Vfksi123",
        "name": "А.Р. Евдокимов"
    }
}

@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username in users and users[username]['password'] == password:
            session['username'] = username
            return jsonify({"success": True, "redirect": url_for('dashboard')})
        else:
            return jsonify({"success": False, "message": "Неверные учетные данные"})
    
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    user = users[session['username']]
    return render_template('dashboard.html', username=session['username'], name=user['name'])

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)