from ..database.models import Personal, Student, Group, Session, engine

def get_personal_count():
    with Session(engine) as session:
        count = session.query(Personal).count()
    return count


def get_students_count():
    with Session(engine) as session:
        count = session.query(Student).count()
    return count


def get_groups_count():
    with Session(engine) as session:
        count = session.query(Group).count()
    return count
