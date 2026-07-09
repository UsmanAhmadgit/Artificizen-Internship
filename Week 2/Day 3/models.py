from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

# Task 1: Create a User model
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    is_active = Column(Boolean, default=True)

    # Relationship to posts
    posts = relationship("Post", back_populates="owner")

# Task 6: Add a Post model with a ForeignKey to User
class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(String)
    
    # The Foreign Key linking to the users table
    owner_id = Column(Integer, ForeignKey("users.id"))

    # Relationship back to the user
    owner = relationship("User", back_populates="posts")