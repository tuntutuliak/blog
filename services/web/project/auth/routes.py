from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from project.auth import bp
from project.models import User
from project import db

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = request.form.get('remember', False)
        
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user, remember=remember)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('main.index'))
        flash('Неверный email или пароль', 'error')
    
    return render_template('auth/login.html')

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        name = request.form.get('name')
        
        if User.query.filter_by(email=email).first():
            flash('Этот email уже зарегистрирован', 'error')
            return redirect(url_for('auth.register'))
        
        user = User(email=email, password=password, name=name)
        db.session.add(user)
        db.session.commit()
        
        login_user(user)
        return redirect(url_for('main.index'))
    
    return render_template('auth/register.html') 