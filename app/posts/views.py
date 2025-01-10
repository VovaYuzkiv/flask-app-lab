import json
import os
from . import post_bp
from flask import render_template, abort, session, flash, redirect, url_for
from .forms import PostForm
from .models import Post, Tag
from app.users.models import User
from app import db

@post_bp.route('/') 
def get_posts():
    stmt = db.select(Post).order_by(Post.id)
    posts = db.session.scalars(stmt).all()
    return render_template("posts.html", posts=posts)

@post_bp.route('/<int:id>') 
def detail_post(id):
    post = db.get_or_404(Post, id)
    if post is None:
        abort(404)
    return render_template("detail_post.html", post=post)

@post_bp.route("/creat_new_post",methods=["GET","POST"])
def creat_new_post():
    form = PostForm()
    form.author_id.choices = [(author.id, author.username) for author in User.query.all()]
    form.tags.choices = [(tag.id, tag.name) for tag in Tag.query.all()]
    if form.validate_on_submit():
        new_post = Post(
            title = form.title.data,
            content = form.content.data,
            posted = form.publish_date.data,
            category = form.category.data,
            aurhor = form.author_id.data,
            author = session.get("user","annonym")
        )
        selected_tags = Tag.query.filter(Tag.id.in_(form.tags.data)).all()
        new_post.tags.extend(selected_tags)

        db.session.add(new_post)
        db.session.commit()
        flash(f"Post {new_post.title} added succsessfully!", "success")
        return redirect ( url_for(".get_posts"))
    return render_template("add_post.html", form=form)

@post_bp.route("/<int:id>/edit_post",methods=["GET","POST"])
def edit_post(id):
    post = db.get_or_404(Post, id)
    form = PostForm(obj=post)
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        post.posted = form.publish_date.data
        post.is_active = form.is_active.data
        post.category = form.category.data
        db.session.commit()
        flash('Post updated succsessfully')
        return redirect(url_for(".detail_post", id=id))
    return render_template("add_post.html", form=form, post=post)
    