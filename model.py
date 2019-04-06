"""Bases and databases"""


import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    user_id = Column(String(50), primary_key=True)
    password = Column(String(50), nullable=False)

    def __repr__(self):
        return f'<User user_id={self.user_id}>'

class Clothing(Base):
    __tablename__ = 'clothes'

    name = Column(String(50), nullable=False)
    article_id = Column(Integer, primary_key=True)
    lot_number = Column(Integer, nullable=False)
    retailer = Column(String(30))
    description = Column(String(250))

    @property
    def serialize(self):
        return {
            'name' : self.name,
            'description' : self.description,
            'article_id' : self.article_id,
            'retailer' : self.retailed
            }


if __name__ == '__main__':
    engine = create_engine('sqlite:///clothingapp.db')
    Base.metadata.create_all(engine)
