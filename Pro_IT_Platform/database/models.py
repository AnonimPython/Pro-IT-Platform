
from typing import List, Optional
from sqlmodel import Relationship, SQLModel, Field, create_engine, Session

class Personal(SQLModel, table=True):
    __tablename__ = "personal"
    id: int = Field(primary_key=True)
    login: str = Field(index=True)
    full_name: str = Field(index=True)
    role: str = Field()
    phone: str = Field()

class Group(SQLModel, table=True):
    __tablename__ = "groups"
    id: int = Field(primary_key=True)
    name: str = Field(index=True) 
    school: str = Field(index=True) 
    course: str = Field(index=True)
    description: str = Field()
    teacher: str = Field(index=True)

    # Связь с моделью Student (один ко многим)
    students: List["Student"] = Relationship(back_populates="group")

class LinksCourses(SQLModel, table=True):
    __tablename__ = "course"
    id: int = Field(primary_key=True)
    name: str = Field(index=True)
    link: str = Field()

class Student(SQLModel, table=True):
    __tablename__ = "students"
    id: int = Field(primary_key=True)
    first_name: str = Field(index=True)
    last_name: str = Field(index=True)
    phone: str = Field(unique=True, index=True)
    login: str = Field()
    password: str = Field()
    school: str = Field(index=True)
    class_number: Optional[int] = Field(default=None)
    course: str = Field()  #* course
    group_id: Optional[int] = Field(default=None, foreign_key="groups.id")
    group: Optional[Group] = Relationship(back_populates="students")

class Module(SQLModel, table=True):
    __tablename__ = "modules"
    id: int = Field(primary_key=True)
    name: str = Field(index=True)  # Название модуля
    course_id: int = Field(foreign_key="courses.id")  # Связь с курсом
    course: Optional["Courses"] = Relationship(back_populates="modules")
    tasks: List["Task"] = Relationship(back_populates="module")  # Связь с заданиями

class Task(SQLModel, table=True):
    __tablename__ = "tasks"
    id: int = Field(primary_key=True)
    text: str = Field()  # Текст задания
    module_id: int = Field(foreign_key="modules.id")  # Связь с модулем
    module: Optional["Module"] = Relationship(back_populates="tasks")

# Обновим модель Courses, чтобы она включала модули
class Courses(SQLModel, table=True):
    __tablename__ = "courses"
    id: int = Field(primary_key=True)
    name: str = Field(index=True)
    link: str = Field()
    modules: List["Module"] = Relationship(back_populates="course")  # Связь с модулями

DATABASE_URL = "sqlite:///pro-it.db"

engine = create_engine(DATABASE_URL)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def add_admin_user():
    # Создаем объект Personal с логином admin
    admin_user = Personal(
        login="admin",
        full_name="Admin User",
        role="administrator",
        phone="1234567890"
    )

    # Открываем сессию и добавляем пользователя
    with Session(engine) as session:
        session.add(admin_user)
        session.commit()  # Сохраняем изменения в базе данных
        print("Пользователь admin успешно добавлен!")


if __name__ == "__main__":
    create_db_and_tables()
    add_admin_user()
    print("База данных и таблицы успешно созданы!")
