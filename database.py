from sqlalchemy import CHAR, Column, ForeignKey, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)

    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def __repr__(self):
        return f" {self.id}, {self.username}, {self.password} "


engine = create_engine("sqlite:///db.sqlite", echo=True)  # makes database in memory
Base.metadata.create_all(
    bind=engine
)  # takes all the classes that extend from base and creates them in the database

Session = sessionmaker(bind=engine)
session = Session()

# in use:
# user1 = User(123, "Bob", "123456")
# session.add(user1)  # with this line of code this user will be created in the database
# session.commit()

# this would be SELECT * FROM users
# data = session.query(User).all()
# print(data)
