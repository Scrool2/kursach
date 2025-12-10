from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Float, Boolean, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.database import Base


class UserRole(str, enum.Enum):
    USER = "USER"
    ADMIN = "ADMIN"


class ArticleCategory(str, enum.Enum):
    POLITICS = "POLITICS"
    TECHNOLOGY = "TECHNOLOGY"
    SPORTS = "SPORTS"
    BUSINESS = "BUSINESS"
    ENTERTAINMENT = "ENTERTAINMENT"
    SCIENCE = "SCIENCE"
    HEALTH = "HEALTH"
    GENERAL = "GENERAL"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(50), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    role = Column(Enum(UserRole), default=UserRole.USER)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    preferences = relationship("UserPreference", back_populates="user", cascade="all, delete-orphan")
    read_history = relationship("ReadHistory", back_populates="user", cascade="all, delete-orphan")


class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(500), nullable=False)
    summary = Column(Text)
    content = Column(Text, nullable=False)
    source_url = Column(String(1000), unique=True, nullable=False)
    image_url = Column(String(1000))
    category = Column(Enum(ArticleCategory), default=ArticleCategory.GENERAL)
    source_id = Column(Integer, ForeignKey("news_sources.id"))
    published_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    source = relationship("NewsSource", back_populates="articles")
    read_history = relationship("ReadHistory", back_populates="article")


class NewsSource(Base):
    __tablename__ = "news_sources"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    url = Column(String(1000), nullable=False)
    website = Column(String(1000))
    category = Column(Enum(ArticleCategory), default=ArticleCategory.GENERAL)
    language = Column(String(10), default="ru")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    articles = relationship("Article", back_populates="source")


class UserPreference(Base):
    __tablename__ = "user_preferences"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    category = Column(Enum(ArticleCategory), nullable=False)
    weight = Column(Float, default=0.5)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    user = relationship("User", back_populates="preferences")


class ReadHistory(Base):
    __tablename__ = "read_history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    article_id = Column(Integer, ForeignKey("articles.id"), nullable=False)
    read_at = Column(DateTime(timezone=True), server_default=func.now())
    read_time_seconds = Column(Integer)

    user = relationship("User", back_populates="read_history")
    article = relationship("Article", back_populates="read_history")