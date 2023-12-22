from sqlalchemy import (
    Column,
    Float,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    create_engine,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)


class Node(Base):
    __tablename__ = "node"

    id = Column(Integer, primary_key=True)
    title = Column(String)

    primary_content = Column(Text)
    secondary_content = Column(Text)

    __table_args__ = Index("title")


class Edge(Base):
    __tablename__ = "edge"

    id = Column(Integer, primary_key=True)

    from_id = Column(Integer, ForeignKey("node.id"))
    to_id = Column(Integer, ForeignKey("node.id"))

    intensity = Column(Float, default=1)

    __table_args__ = Index("from_id", "to_id", "intensity")


engine = create_engine("sqlite:///db.sqlite", echo=True)
Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()
