from sqlalchemy import create_engine, Table, Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.orm import declarative_base, relationship

eng = create_engine('sqlite:///movies.db')
Base = declarative_base()


user_series = Table(
    "user_series",
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('series_id', Integer, ForeignKey('series.id')),
)

user_movies = Table(
    "user_movies",
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('movies_id', Integer, ForeignKey('movies.id')),
)

watching_list_series = Table(
    "watching_list_series",
    Base.metadata,
    Column('watching_list_id', Integer, ForeignKey('watching_list.id')),
    Column('series_id', Integer, ForeignKey('series.id')),
)

watching_list_movies = Table(
    "watching_list_movies",
    Base.metadata,
    Column('watching_list_id', Integer, ForeignKey('watching_list.id')),
    Column('movies_id', Integer, ForeignKey('movies.id')),
)


class Movie(Base):
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(80), nullable=False)
    rating = Column(Integer, nullable=False)
    release_year = Column(String(4), nullable=False)

    user = relationship("User", secondary=user_movies, back_populates="movies")
    watching_lists = relationship(
        "WatchingList", secondary=watching_list_movies, back_populates="movies")


class Series(Base):
    __tablename__ = 'series'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(80), nullable=False)
    rating = Column(Integer, nullable=False)
    release_year = Column(String(4), nullable=False)
    amount_of_seasons = Column(Integer, nullable=False)

    user = relationship("User", secondary=user_series, back_populates="series")
    watching_lists = relationship(
        "WatchingList", secondary=watching_list_series, back_populates="series")


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(20), nullable=False)
    surname = Column(String(20), default="")

    watch_lists = relationship(
        "WatchingList", back_populates="user", cascade="all, delete-orphan")
    movies = relationship("Movie", secondary=user_movies,
                          back_populates="user")
    series = relationship("Series", secondary=user_series,
                          back_populates="user")


class WatchingList(Base):
    __tablename__ = "watching_list"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(20), nullable=False)
    date_when_created = Column(String(20), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="watch_lists")

    movies = relationship("Movie", secondary=watching_list_movies,
                          back_populates="watching_lists")
    series = relationship("Series", secondary=watching_list_series,
                          back_populates="watching_lists")


if __name__ == "__main__":
    Base.metadata.create_all(eng)
