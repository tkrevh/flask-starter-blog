from . import app, db
from flask import render_template, flash, request, session, redirect, url_for, abort
from flask.ext.security import login_required, current_user
from flask_wtf import Form
from content.models import Tag, Comment, Post
from content.forms import PostForm, CommentForm


@app.route("/")
def index():
    posts = Post.query.order_by("created_at desc").all()
    return render_template("index.html", posts=posts)

    
@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post()
        form.populate_obj(post)
        post.author_id = current_user.id
        db.session.add(post)
        db.session.commit()
        flash("New Post successfully created")
        return redirect(url_for("index"))
    return render_template("content/new_post.html", form=form)
    
@app.route("/post/edit/<id>/", methods=['GET', 'POST'])
@login_required
def edit_post(id):
    post = Post.query.get_or_404(id)
    form = PostForm(obj=post)

    if form.validate_on_submit():
        form.populate_obj(post)
        db.session.add(post)
        db.session.commit()
        flash("Post successfully updated")
        return redirect(url_for("index"))
    return render_template("content/edit_post.html", form=form, id=post.id)    
    
@app.route("/post/view/<id>/", methods=['GET', 'POST'])
def view_post(id):
    post = Post.query.get_or_404(id)
    form = CommentForm()
    
    if form.validate_on_submit():
        if not current_user.can_comment:
          abort(404)
        comment = Comment()
        form.populate_obj(comment)
        comment.author_id = current_user.id
        comment.post_id = post.id
        db.session.add(comment)
        db.session.commit()
        flash("New Comment successfully added")
        return redirect(url_for("view_post", id=post.id))
    return render_template("content/view_post.html", post=post, form=form)
    
