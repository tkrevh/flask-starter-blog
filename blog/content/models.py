from .. import app, db, api
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

# Define models
post_tags = db.Table('post_tags',
    db.Column('post_id', db.Integer(), db.ForeignKey('post.id')),
    db.Column('tag_id', db.Integer(), db.ForeignKey('tag.id'))
)

class Comment(db.Model):
    __tablename__ = 'comment'
    
    id = db.Column(db.Integer(), primary_key=True)
    text = db.Column(db.String(1024))
    created_at = db.Column(db.DateTime(), default=db.func.current_timestamp())
    author_id = db.Column(db.Integer, ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, ForeignKey('post.id'), nullable=False)

    def __str__(self):
        return self.text[:40]


class Tag(db.Model):
    __tablename__ = 'tag'
    
    id = db.Column(db.Integer(), primary_key=True)
    text = db.Column(db.String(32))
    created_at = db.Column(db.DateTime(), default=db.func.current_timestamp())

    def __str__(self):
        return self.text


class Post(db.Model):
    __tablename__ = 'post'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    text = db.Column(db.String(4096))
    author_id = db.Column(db.Integer, ForeignKey('user.id'), nullable=False)
    comments = db.relationship("Comment", backref='posts', order_by="desc(Comment.created_at)")
    tags = db.relationship('Tag', secondary=post_tags,
                            backref=db.backref('posts', lazy='dynamic'))
    created_at = db.Column(db.DateTime(), default=db.func.current_timestamp())        

    def __str__(self):
        return self.title

