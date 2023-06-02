# main.py
from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash
from .models import ForumPost, ForumThread, User
import os
from . import db, app

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.username)

@main.route('/forum', methods=['POST', 'GET'])
@login_required
def forum():
    current_u = current_user
    threads = ForumThread.query.all()
    if request.method == 'POST':
        new_thread = ForumThread(user_id=current_user.id, subject=request.form.get('thread_subject'))
        db.session.add(new_thread)
        db.session.commit()
        threads = ForumThread.query.all()
    return render_template('forum.html', threads=threads, current_user=current_u)

@main.route('/forum/<int:thread_id>', methods=['POST', 'GET'])
@login_required
def single_forum_post(thread_id):
    current_u = current_user
    thread = ForumThread.query.filter_by(id=thread_id).first()
    post_and_answers = ForumPost.query.filter_by(thread_id=thread_id)
    photo_url = url_for('static', filename='profile_pics/'+thread.user_thread.photo)
    if request.method == 'POST':
        new_post = ForumPost(user_id=current_user.id, thread_id=thread_id, contents=request.form.get('post_answer'))
        db.session.add(new_post)
        db.session.commit()
    return render_template('single_forum_post.html', post_and_answers=post_and_answers, thread=thread,
                           current_user=current_u, photo_url=photo_url)

@main.route('/foo', methods=['GET', 'POST'])
def foo():
    if request.method == 'POST':
        post_id = request.form.get('post_id')
        forum_post = ForumPost.query.filter_by(id=post_id).first()
        if current_user.id == forum_post.user_id:
            db.session.delete(forum_post)
            db.session.commit()
        return redirect(url_for('.single_forum_post', thread_id=forum_post.thread_id))

@main.route('/foo_threads', methods=['GET', 'POST'])
def foo_threads():
    if request.method == 'POST':
        thread_id = request.form.get('thread_id')
        thread = ForumThread.query.filter_by(id=thread_id).first()
        if current_user.id == thread.user_id:
            db.session.delete(thread)
            db.session.commit()
        return redirect(url_for('.forum'))

@main.route('/profile/change_profile', methods=['GET', 'POST'])
def change_profile():
    current_u = current_user
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")
        email = request.form.get("email")
        age = request.form.get("age")
        bio = request.form.get("bio")
        photo = request.files["photo"]
        picture_path = os.path.join(app.root_path, 'static\profile_pics', photo.filename)
        photo.save(picture_path)
        num_rows_updated = User.query.filter_by(id=current_user.id).update(dict(username=username,
                                                                                password=generate_password_hash(password, method='sha256'),
                                                                                email=email, age=age, bio=bio, photo=photo.filename))
        db.session.commit()
    return render_template('change_profile.html', current_user=current_u)

### problemy -> redirect do dynamic urlsów, obsługa wielu różnych postów na jednym widoku, problemy z cssem
### ogarnięcie query sqlalchemy
### dodawanie zdjęć