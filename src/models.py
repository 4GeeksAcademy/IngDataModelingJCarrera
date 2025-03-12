import os
import sys
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from eralchemy2 import render_er

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(250), nullable=False, unique=True)
    firstname = Column(String(10), nullable=False)
    lastname = Column(String(10), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    
    posts = relationship("Post", back_populates="user")
    comments = relationship("Comment", back_populates="user")

class Post(Base):
    __tablename__ = 'post'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    img_url = Column(String(250), nullable=False)
    likes_count = Column(Integer, nullable=False)

    user = relationship("User", back_populates="posts")
    comments = relationship("Comment", back_populates="post")
    medias = relationship("Media", back_populates="post")

class Comment(Base):
    __tablename__ = 'comment'
    id = Column(Integer, primary_key=True)
    comment_text = Column(String(250), nullable=False)
    author_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    post_id = Column(Integer, ForeignKey("post.id"), nullable=False)

    user = relationship("User", back_populates="comments")
    post = relationship("Post", back_populates="comments")

    def to_dict(self):
        return {}

class Media(Base):
    __tablename__ = 'media'
    id = Column(Integer, primary_key=True)
    type = Column(String(250), nullable=False)
    url = Column(String(250), nullable=False)
    post_id = Column(Integer, ForeignKey("post.id"), nullable=False)
    
    post = relationship("Post", back_populates="medias")

class Follower(Base):
    __tablename__ = 'follower'
    user_from_id = Column(Integer, ForeignKey("user.id"), primary_key=True)
    user_to_id = Column(Integer, ForeignKey("user.id"), primary_key=True)

    followers = relationship("User", foreign_keys=[user_from_id], backref="followings")
    followings = relationship("User", foreign_keys=[user_to_id], backref="followers")

## Draw from SQLAlchemy base
try:
    result = render_er(Base, 'diagram.png')
    print("Success! Check the diagram.png file")
except Exception as e:
    print("There was a problem generating the diagram")
    raise e
