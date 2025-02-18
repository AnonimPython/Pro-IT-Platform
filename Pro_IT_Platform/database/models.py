
from sqlmodel import SQLModel, Field, create_engine

class Personal(SQLModel, table=True):
    __tablename__ = "personal"
    id: int = Field(primary_key=True)
    login: str = Field(index=True)

class Courses(SQLModel, table=True):
    __tablename__ = "courses"
    id: int = Field(primary_key=True)
    name: str = Field(index=True)
    link: str = Field()

class Student(SQLModel, table=True):
    __tablename__ = "students"
    id: int = Field(primary_key=True)
    first_name: str = Field(index=True)
    last_name: str = Field(index=True)
    phone: str = Field(unique=True, index=True)
    school: str = Field(index=True)
    class_number: int = Field(index=True)


DATABASE_URL = "sqlite:///pro-it.db"

engine = create_engine(DATABASE_URL)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

if __name__ == "__main__":
    create_db_and_tables()
    print("База данных и таблицы успешно созданы!")
