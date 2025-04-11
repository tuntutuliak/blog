from flask import render_template, request, redirect, url_for, flash
from project.models import Post, Category, Tag, Comment
from project import db
from datetime import datetime
from project.blog import bp

# Временные данные для демонстрации
posts = [
    {
        'id': 1,
        'title': 'Why Choose Cruises Instead of Tours',
        'category': 'News',
        'date': datetime(2018, 4, 21, 12, 5),
        'image': 'images/sidebar-blog-1-370x264.jpg'
    },
    {
        'id': 2,
        'title': '5 Adventure Cruises You Cannot Miss',
        'category': 'News',
        'date': datetime(2018, 4, 21, 12, 5),
        'image': 'images/sidebar-blog-2-370x264.jpg'
    },
    # Добавьте больше постов по необходимости
]

archives = [
    {'year': 2018, 'month': 5, 'name': 'May 2018'},
    {'year': 2018, 'month': 4, 'name': 'April 2018'},
    {'year': 2018, 'month': 3, 'name': 'March 2018'},
    {'year': 2018, 'month': 2, 'name': 'February 2018'},
    {'year': 2018, 'month': 1, 'name': 'January 2018'},
]

categories = [
    {'name': 'News'},
    {'name': 'Cruises'},
    {'name': 'Traveling'},
    {'name': 'Tips'},
    {'name': 'Ships'},
]

tags = [
    {'name': 'Cruises'},
    {'name': 'Tips'},
    {'name': 'Ships'},
    {'name': 'Recommendations'},
    {'name': 'Traveling'},
    {'name': 'News'},
]

about_text = 'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam'

@bp.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.created_at.desc()).paginate(page=page, per_page=6)
    categories = Category.query.all()
    tags = Tag.query.all()
    return render_template('blog/index.html', posts=posts, categories=categories, tags=tags)

@bp.route('/grid')
def grid():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.created_at.desc()).paginate(page=page, per_page=9)
    categories = Category.query.all()
    tags = Tag.query.all()
    return render_template('blog/grid.html', posts=posts, categories=categories, tags=tags)

@bp.route('/sidebar')
def sidebar():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.created_at.desc()).paginate(page=page, per_page=6)
    categories = Category.query.all()
    tags = Tag.query.all()
    popular_posts = Post.query.order_by(Post.created_at.desc()).limit(5).all()
    return render_template('blog/sidebar.html', 
                         posts=posts, 
                         categories=categories, 
                         tags=tags,
                         popular_posts=popular_posts)

@bp.route('/<int:post_id>')
def post(post_id):
    post = Post.query.get_or_404(post_id)
    categories = Category.query.all()
    tags = Tag.query.all()
    comments = Comment.query.filter_by(post_id=post_id).order_by(Comment.created_at.desc()).all()
    return render_template('blog/post.html', 
                         post=post, 
                         categories=categories, 
                         tags=tags,
                         comments=comments)

@bp.route('/category/<category>')
def category(category):
    category = Category.query.filter_by(name=category).first_or_404()
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter_by(category=category).order_by(
        Post.created_at.desc()).paginate(page=page, per_page=6)
    categories = Category.query.all()
    tags = Tag.query.all()
    return render_template('blog/index.html', 
                         posts=posts, 
                         categories=categories, 
                         tags=tags,
                         current_category=category)

@bp.route('/tag/<tag_name>')
def tag(tag_name):
    tag = Tag.query.filter_by(name=tag_name).first_or_404()
    page = request.args.get('page', 1, type=int)
    posts = Post.query.join(post_tags).filter(post_tags.c.tag_id == tag.id).order_by(Post.created_at.desc()).paginate(page=page, per_page=6)
    categories = Category.query.all()
    tags = Tag.query.all()
    return render_template('blog/index.html', 
                         posts=posts, 
                         categories=categories, 
                         tags=tags,
                         current_tag=tag)

@bp.route('/<int:post_id>/comment', methods=['POST'])
def add_comment(post_id):
    post = Post.query.get_or_404(post_id)
    
    if not request.form.get('first_name') or \
       not request.form.get('last_name') or \
       not request.form.get('email') or \
       not request.form.get('content'):
        flash('Пожалуйста, заполните все поля', 'error')
        return redirect(url_for('blog.post', post_id=post_id))
    
    comment = Comment(
        first_name=request.form['first_name'],
        last_name=request.form['last_name'],
        email=request.form['email'],
        content=request.form['content'],
        post_id=post_id
    )
    db.session.add(comment)
    db.session.commit()
    
    flash('Ваш комментарий добавлен!', 'success')
    return redirect(url_for('blog.post', post_id=post_id))

@bp.route('/archive/<int:year>/<int:month>')
def archive(year, month):
    start_date = datetime(year, month, 1)
    if month == 12:
        end_date = datetime(year + 1, 1, 1)
    else:
        end_date = datetime(year, month + 1, 1)
    
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter(
        Post.created_at >= start_date,
        Post.created_at < end_date
    ).order_by(Post.created_at.desc()).paginate(page=page, per_page=6)
    
    categories = Category.query.all()
    tags = Tag.query.all()
    return render_template('blog/index.html', 
                         posts=posts, 
                         categories=categories, 
                         tags=tags,
                         archive_date=start_date)

@bp.route('/search')
def search():
    query = request.args.get('q', '')
    page = request.args.get('page', 1, type=int)
    
    posts = Post.query.filter(
        Post.title.ilike(f'%{query}%') | 
        Post.content.ilike(f'%{query}%')
    ).order_by(Post.created_at.desc()).paginate(page=page, per_page=6)
    
    categories = Category.query.all()
    tags = Tag.query.all()
    return render_template('blog/index.html', 
                         posts=posts, 
                         categories=categories, 
                         tags=tags,
                         search_query=query) 