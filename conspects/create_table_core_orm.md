# SQLAlchemy 2.0: Создание таблиц через Core и ORM

## 1. Основные импорты

```python
from sqlalchemy import (
    MetaData, Table, Column, Integer, String, DateTime, 
    Boolean, Float, Text, ForeignKey, create_engine
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from datetime import datetime
from typing import Optional
```

## 2. Создание таблиц через Core

### 2.1 Базовая настройка MetaData

```python
# Создаем объект MetaData для хранения информации о схеме
metadata = MetaData()
```

### 2.2 Определение таблицы users

```python
users_table = Table(
    'users',  # имя таблицы
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('username', String(50), unique=True, nullable=False),
    Column('email', String(100), unique=True, nullable=False),
    Column('password_hash', String(255), nullable=False),
    Column('first_name', String(50), nullable=True),
    Column('last_name', String(50), nullable=True),
    Column('age', Integer, nullable=True),
    Column('is_active', Boolean, default=True),
    Column('salary', Float, nullable=True),
    Column('bio', Text, nullable=True),
    Column('created_at', DateTime, default=func.now(), nullable=False),
    Column('updated_at', DateTime, default=func.now(), onupdate=func.now())
)
```

### 2.3 Определение таблицы posts с внешним ключом

```python
posts_table = Table(
    'posts',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('title', String(200), nullable=False),
    Column('content', Text, nullable=False),
    Column('user_id', Integer, ForeignKey('users.id'), nullable=False),
    Column('views_count', Integer, default=0),
    Column('is_published', Boolean, default=False),
    Column('rating', Float, default=0.0),
    Column('published_at', DateTime, nullable=True),
    Column('created_at', DateTime, default=func.now()),
    Column('updated_at', DateTime, default=func.now(), onupdate=func.now())
)
```

### 2.4 Создание таблиц в базе данных (Core)

```python
# Создание всех таблиц
def create_tables_core(engine):
    metadata.create_all(engine)
    print("Таблицы созданы через Core")

# Удаление всех таблиц
def drop_tables_core(engine):
    metadata.drop_all(engine)
    print("Таблицы удалены через Core")
```

## 3. Создание таблиц через ORM

### 3.1 Базовая настройка для ORM 2.0

```python
# Базовый класс для всех ORM моделей
class Base(DeclarativeBase):
    pass
```

### 3.2 Определение модели User

```python
class User(Base):
    __tablename__ = 'users'
    
    # Способ 1: Современный подход с Mapped и mapped_column
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    
    # Опциональные поля
    first_name: Mapped[Optional[str]] = mapped_column(String(50))
    last_name: Mapped[Optional[str]] = mapped_column(String(50))
    age: Mapped[Optional[int]] = mapped_column(Integer)
    salary: Mapped[Optional[float]] = mapped_column(Float)
    bio: Mapped[Optional[str]] = mapped_column(Text)
    
    # Boolean с значением по умолчанию
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    
    # Поля времени
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, 
        default=func.now(), 
        onupdate=func.now()
    )
    
    # Связь с постами (один ко многим)
    posts: Mapped[list["Post"]] = relationship("Post", back_populates="user")
    
    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', email='{self.email}')>"
```

### 3.3 Определение модели Post

```python
class Post(Base):
    __tablename__ = 'posts'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    
    # Внешний ключ
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    
    # Поля с значениями по умолчанию
    views_count: Mapped[int] = mapped_column(Integer, default=0)
    is_published: Mapped[bool] = mapped_column(Boolean, default=False)
    rating: Mapped[float] = mapped_column(Float, default=0.0)
    
    # Опциональные поля
    published_at: Mapped[Optional[datetime]] = mapped_column(DateTime)
    
    # Поля времени
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, 
        default=func.now(), 
        onupdate=func.now()
    )
    
    # Связь с пользователем (многие к одному)
    user: Mapped["User"] = relationship("User", back_populates="posts")
    
    def __repr__(self):
        return f"<Post(id={self.id}, title='{self.title}', user_id={self.user_id})>"
```

### 3.4 Альтернативный способ определения ORM модели (классический)

```python
class UserClassic(Base):
    __tablename__ = 'users_classic'
    
    # Способ 2: Классический подход без типизации
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    first_name = Column(String(50))
    last_name = Column(String(50))
    age = Column(Integer)
    is_active = Column(Boolean, default=True)
    salary = Column(Float)
    bio = Column(Text)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
```

### 3.5 Создание таблиц в базе данных (ORM)

```python
# Создание всех таблиц
def create_tables_orm(engine):
    Base.metadata.create_all(engine)
    print("Таблицы созданы через ORM")

# Удаление всех таблиц
def drop_tables_orm(engine):
    Base.metadata.drop_all(engine)
    print("Таблицы удалены через ORM")
```

## 4. Полные примеры использования

### 4.1 Пример создания таблиц через Core

```python
from sqlalchemy import create_engine

# Предполагаем, что engine уже создан
# engine = create_engine("sqlite:///example.db")

def example_core_tables(engine):
    """Полный пример работы с Core"""
    
    # Создаем таблицы
    metadata.create_all(engine)
    
    # Проверяем созданные таблицы
    print("Созданы таблицы:", list(metadata.tables.keys()))
    
    # Информация о колонках таблицы users
    print("\nКолонки таблицы users:")
    for column in users_table.columns:
        print(f"- {column.name}: {column.type} (nullable: {column.nullable})")
```

### 4.2 Пример создания таблиц через ORM

```python
def example_orm_tables(engine):
    """Полный пример работы с ORM"""
    
    # Создаем таблицы
    Base.metadata.create_all(engine)
    
    # Проверяем созданные таблицы
    print("Созданы таблицы:", list(Base.metadata.tables.keys()))
    
    # Информация о модели User
    print(f"\nТаблица модели User: {User.__tablename__}")
    print("Колонки:")
    for column_name, column in User.__table__.columns.items():
        print(f"- {column_name}: {column.type}")
```

## 5. Расширенные примеры с дополнительными типами данных

### 5.1 Таблица с более сложными типами данных

```python
from sqlalchemy import JSON, DECIMAL, Date, Time, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from decimal import Decimal
import uuid

# Расширенная таблица через Core
products_table = Table(
    'products',
    metadata,
    Column('id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    Column('name', String(100), nullable=False),
    Column('price', DECIMAL(10, 2), nullable=False),  # Точная десятичная арифметика
    Column('description', Text),
    Column('metadata_json', JSON),  # JSON поле
    Column('launch_date', Date),    # Только дата
    Column('launch_time', Time),    # Только время
    Column('created_timestamp', TIMESTAMP, default=func.now()),
    Column('tags', ARRAY(String)),  # Массив строк (PostgreSQL)
    Column('is_available', Boolean, default=True)
)

# Расширенная модель через ORM
class Product(Base):
    __tablename__ = 'products_orm'
    
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    price: Mapped[Decimal] = mapped_column(DECIMAL(10, 2), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    metadata_json: Mapped[Optional[dict]] = mapped_column(JSON)
    launch_date: Mapped[Optional[datetime]] = mapped_column(Date)
    created_timestamp: Mapped[datetime] = mapped_column(TIMESTAMP, default=func.now())
    is_available: Mapped[bool] = mapped_column(Boolean, default=True)
```

## 6. Практические советы и лучшие практики

### 6.1 Соглашения об именовании

```python
# Хорошие практики именования:
class UserProfile(Base):
    __tablename__ = 'user_profiles'  # snake_case для имен таблиц
    
    # Используйте понятные имена колонок
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    profile_image_url: Mapped[Optional[str]] = mapped_column(String(500))
    date_of_birth: Mapped[Optional[datetime]] = mapped_column(Date)
    
    # Всегда добавляйте created_at и updated_at
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())
```

### 6.2 Индексы и ограничения

```python
from sqlalchemy import Index, UniqueConstraint, CheckConstraint

class UserWithConstraints(Base):
    __tablename__ = 'users_with_constraints'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(100), nullable=False)
    age: Mapped[Optional[int]] = mapped_column(Integer)
    
    # Определение ограничений на уровне таблицы
    __table_args__ = (
        UniqueConstraint('username', 'email', name='unique_username_email'),
        CheckConstraint('age >= 0 AND age <= 150', name='check_age_range'),
        Index('idx_username_email', 'username', 'email'),  # Составной индекс
    )
```