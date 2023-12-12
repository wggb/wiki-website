from sqlalchemy import CHAR, Column, ForeignKey, Integer, String, Text, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)


class MarkdownFile(Base):
    __tablename__ = "markdown_files"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    content = Column(Text)


engine = create_engine("sqlite:///db.sqlite", echo=True)
Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()
