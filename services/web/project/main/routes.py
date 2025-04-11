from flask import Blueprint, render_template, request, redirect, url_for, flash
from project.main import bp
from project.models import Post, Category, Tag
from project import db

@bp.route('/')
def index():
    featured_posts = Post.query.order_by(Post.created_at.desc()).limit(2).all()
    latest_posts = Post.query.order_by(Post.created_at.desc()).limit(4).all()
    categories = Category.query.all()
    tags = Tag.query.all()
    popular_posts = Post.query.order_by(Post.created_at.desc()).limit(5).all()
    
    return render_template('main/index.html',
                          featured_posts=featured_posts,
                          latest_posts=latest_posts,
                          categories=categories,
                          tags=tags,
                          popular_posts=popular_posts)

@bp.route('/about')
def about():
    latest_posts = Post.query.order_by(Post.created_at.desc()).limit(4).all()
    return render_template('main/about.html', latest_posts=latest_posts)

@bp.route('/cruises')
def cruises():
    return render_template('main/cruises.html')

@bp.route('/single-cruise')
def single_cruise():
    return render_template('main/single-cruise.html')

@bp.route('/contacts')
def contacts():
    return render_template('main/contacts.html')

@bp.route('/contact', methods=['POST'])
def contact():
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    email = request.form.get('email')
    phone = request.form.get('phone')
    message = request.form.get('message')
    
    # Здесь можно добавить логику отправки email или сохранения в базу данных
    
    flash('Спасибо за ваше сообщение! Мы свяжемся с вами в ближайшее время.', 'success')
    return redirect(url_for('main.contacts'))

@bp.route('/gallery')
def gallery():
    return render_template('main/gallery.html')

@bp.route('/careers')
def careers():
    return render_template('main/careers.html')

@bp.route('/history')
def history():
    return render_template('main/history.html')

@bp.route('/booking')
def booking():
    return render_template('main/booking.html')

@bp.route('/terms')
def terms():
    return render_template('main/terms.html')

@bp.route('/privacy')
def privacy():
    return render_template('main/privacy.html')

@bp.route('/search')
def search():
    query = request.args.get('q', '')
    # Здесь будет логика поиска
    return render_template('main/search-results.html', query=query)

@bp.route('/book', methods=['POST'])
def book():
    check_in = request.form.get('check_in')
    check_out = request.form.get('check_out')
    guests = request.form.get('guests')
    # Здесь будет логика бронирования
    return redirect(url_for('main.booking'))

@bp.route('/category/<int:category_id>')
def category(category_id):
    category = Category.query.get_or_404(category_id)
    posts = Post.query.filter_by(category_id=category_id).order_by(Post.created_at.desc()).all()
    categories = Category.query.all()
    tags = Tag.query.all()
    
    return render_template('main/category.html',
                          category=category,
                          posts=posts,
                          categories=categories,
                          tags=tags) 