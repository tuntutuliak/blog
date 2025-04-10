from flask import render_template, redirect, url_for, flash, request
from project.auth import bp

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Здесь будет логика аутентификации
        return redirect(url_for('main.index'))
    return render_template('auth/login.html')

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Здесь будет логика регистрации
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html') 