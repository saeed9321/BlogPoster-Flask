from flask import render_template, flash, redirect, url_for, request
from project import app, db
from werkzeug.security import generate_password_hash, check_password_hash
from project.forms import LoginForm, RegistrationForm, UpdateForm, BlogForm, UploadImage
from project.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.utils import secure_filename
import os

allowed_extensions = ['png', 'jpg', 'jpeg', 'bmp']

def check_if_allowed(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

@app.route('/delete/<post_id>')
@login_required
def delete(post_id):
    post = Post.query.get_or_404(post_id)
    if current_user.id == post.author.id:
        db.session.delete(post)
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/index')
def index():
    posts = Post.query.all()
    return render_template('index.html', posts=posts)

@app.route('/new', methods=['post', 'get'])
@login_required
def new():
    new_post = BlogForm()
    if new_post.validate_on_submit():
        post = Post(title=request.form.get('title'), content=request.form.get('content'), user_id=current_user.id)
        db.session.add(post)
        db.session.commit()
        flash('New post submitted', 'success')
        return redirect(url_for('index'))
    return render_template('post.html', new_post=new_post)

@app.route('/login', methods=['get', 'post'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            flash(f'Successfully logged in as {form.username.data}!', 'success')
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash(f'Bad Username or Password', 'danger')
    return render_template('login.html', title="Login Page", form=form)

@app.route('/register', methods=['post', 'get'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        if User.query.filter_by(username=form.username.data).first():
            flash("This Username already exists", "danger")
        elif User.query.filter_by(email=form.email.data).first():
            flash("Already have an account with this Email", "danger")
        else:
            flash(f'Successfully registered in as {form.username.data}!', 'success')
            user = User(username=form.username.data, password=generate_password_hash(form.password.data), email=form.email.data)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('index'))
    return render_template('register.html', title="Registration page", form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/account', methods=['post', 'get'])
@login_required
def account():
    posts = len(current_user.posts)
    update_form = UpdateForm()
    form = UploadImage()
    img_file = url_for('static', filename=current_user.profile_image)
    if form.validate_on_submit():
        image = request.files['file']
        new_image = secure_filename(image.filename)
        if check_if_allowed(new_image) is True:
            image.save(os.path.join(app.config['upload'] + os.sep + 'static', new_image))
            user = User.query.filter_by(username=current_user.username).first()
            user.profile_image = new_image
            db.session.commit()
        else:
            flash('Unsupported file', 'danger')
        return redirect(url_for('account'))
    return render_template('account.html', posts=posts, form=form, title="Account page", image=img_file)

