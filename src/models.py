import os
import sys
from sqlalchemy.orm import declarative_base, Mapped, mapped_column, relationship 
from sqlalchemy import create_engine
from eralchemy2 import render_er
from sqalchemy  import Integer, String, ForeignKey

Base = declarative_base()

class User (Base):
    __tablename__ = 'user'
    id:Mapped[int]=mapped_column(Integer, primary_key=True)
    username:Mapped[str]=mapped_column( String(250), nullable=False, unique=True)
    firstname:Mapped[str]=mapped_column(String(10), nullable=False )
    lastname:Mapped[str]=mapped_column(String(10), nullable=False)
    email:Mapped[str]=mapped_column(String(100), nullable=False, unique=True)
    
    posts: Mapped["Post"]=relationship(back_populates="user")
    comments: Mapped["Comment"]=relationship(back_populates="user")
    


class Post (Base):
    __tablename__ = 'post'
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    img_url: Mapped[str] = mapped_column(String(250), nullable=False) 
    likes_count: Mapped[int] = mapped_column(Integer, nullable=False)

    user: Mapped["User"]= relationship(back_populates="posts")
    comments: Mapped["Comment"]=relationship(back_populates="post")
    medias: Mapped["Media"]= relationship(back_populates="post")

    


class Comment(Base):
    __tablename__='comment'
    id:Mapped[int]=mapped_column(Integer, primary_key=True)
    comment_text:Mapped [str]=mapped_column(String(250), nullable=False)
    author_id:Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    post_id:Mapped[int] = mapped_column(ForeignKey("post.id"), nullable=False) 

    user: Mapped["User"]= relationship(back_populates="comments")
    post: Mapped["Post"]= relationship(back_populates="comments")

    def to_dict(self):
        return {}
    
class Media (Base):
    __tablename__='media'
    id:Mapped[int]=mapped_column(Integer, primary_key=True)
    type:Mapped[str]=mapped_column(String(250), nullable=False)
    url:Mapped[str]=mapped_column(String(250), nullable=False)
    post_id:Mapped[int] = mapped_column(ForeignKey("post.id"), nullable=False) 
    
    post: Mapped["Post"]= relationship(back_populates="medias")

class Follower (Base):
    __tablename__='follower'
    user_from_id:Mapped[int]=mapped_column(Integer, primary_key=True)
    user_to_id:Mapped[int]=mapped_column(Integer, primary_key=True)

    followers:Mapped["User"]=relationship(backref="followings")
    followings:Mapped["User"]=relationship(backref="followers")

        
    
 

## Draw from SQLAlchemy base
try:
    result = render_er(Base, 'diagram.png')
    print("Success! Check the diagram.png file")
except Exception as e:
    print("There was a problem genering the diagram")
    raise e
