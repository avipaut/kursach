from flask import Flask, redirect, url_for
from flask_socketio import SocketIO
from flask_cors import CORS
import os
from routes.documents import documents_bp
from routes.chat import chat_bp, socketio
from routes.zoom import zoom_bp
from routes.reports import reports_bp
from routes.kpi import kpi_bp
from routes.auth import auth_bp  # Новый модуль для регистрации/авторизации

app = Flask(__name__)
CORS(app)  # Разрешаем все кросс-доменные запросы
socketio.init_app(app, cors_allowed_origins="*")

# Подключаем Blueprints
app.register_blueprint(documents_bp, url_prefix='/documents')
app.register_blueprint(chat_bp, url_prefix='/chat')
app.register_blueprint(zoom_bp, url_prefix='/zoom')
app.register_blueprint(reports_bp, url_prefix='/reports')
app.register_blueprint(kpi_bp, url_prefix='/kpi')
app.register_blueprint(auth_bp, url_prefix='/auth')  # Регистрация auth Blueprint

# Добавление корневого маршрута
@app.route('/')
def index():
    return redirect(url_for('auth.login'))  # Перенаправляем на страницу авторизации

UPLOAD_FOLDER = "uploaded_documents"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.secret_key = 'your_secret_key_here'  # Замените на свой ключ для сессий

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
