import sys
import datetime
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text,\
    Boolean, Table, ForeignKey, Date, Time
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

sys.path.append(".")

from config import DATABASE


engine = create_engine(
    f'{DATABASE["drivername"]}+psycopg2://{DATABASE["username"]}:{DATABASE["password"]}@{DATABASE["host"]}/{DATABASE["database"]}')

Base = declarative_base()


"""Отношения многие ко многим группы и класс ученика который учатся в этих группах"""
group_mtm_grade = Table('group_grade', Base.metadata,
                    Column('group_id', ForeignKey('group.id')),
                    Column('grade_id', ForeignKey('grade.id')))



class Teacher(Base):
    """Учителя"""
    __tablename__ = 'teacher'

    id = Column(Integer(), primary_key=True)
    first_name = Column(String(15), nullable=False)
    last_name = Column(String(20), nullable=False)
    email = Column(String(100))
    town = Column(String(40))
    description = Column(Text())

    def __repr__(self) -> str:
        return '{} {}'.format(self.first_name, self.last_name)


class Group(Base):
    """Группы с кол-вом учеников, вариантом оплаты занятия"""
    __tablename__ = 'group'
    id = Column(Integer(), primary_key=True)
    name = Column(String(100), nullable=False)
    quota = Column(Integer(), nullable=False)
    sublease = Column(Boolean(), nullable=False, default=False)  # Субаренда
    price = Column(Integer(), nullable=False)
    duration = Column(Integer(), nullable=False)
    description = Column(Text())
    is_online = Column(Boolean(), nullable=False, default=False)  # False - офлайн

    teacher_id = Column(Integer(), ForeignKey('teacher.id'))
    teacher = relationship('Teacher', backref='group')
    grade = relationship('Grade', secondary=group_mtm_grade, backref='group')

    def __repr__(self) -> str:
        return '{} {}'.format(self.name, self.quota)


class Grade(Base):
    """Класс в котором учатся ученики,
    0 - дошкольник, 12 - студент, 13 - взрослый"""
    __tablename__ = 'grade'
    id = Column(Integer(), primary_key=True)
    name = Column(Integer(), nullable=False)

    def __repr__(self) -> str:
        return str(self.name)


class User(Base):
    """Ученики"""
    __tablename__ = 'user'
    id = Column(Integer(), primary_key=True)
    first_name = Column(String(15), nullable=False)
    last_name = Column(String(20), nullable=False)
    town = Column(String(40))
    description = Column(Text())
    birthday = Column(Date())
    phone_number = Column(String(15))
    is_active = Column(Boolean(), nullable=False, default=True)
    created_on = Column(DateTime(), default=lambda: datetime.datetime.now())
    updated_on = Column(DateTime(),
                        default=lambda: datetime.datetime.now(),
                        onupdate=lambda: datetime.datetime.now())
    
    group_id = Column(Integer(), ForeignKey('group.id'))
    group = relationship('Group', backref='user')


class ClassRoom(Base):
    """Кабинет может быть онлайн"""
    __tablename__ = 'class_room'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    location = Column(String(20), nullable=False)
    description = Column(Text())


class ClassTime(Base):
    """Время занятий, занятия могут идти одна за одной"""
    __tablename__ = 'class_time'
    id = Column(Integer(), primary_key=True)
    isoweekday = Column(Integer(), nullable=False)  # день недели 1-пн, 7-вс
    start_time = Column(Time(), nullable=False)
    end_time = Column(Time(), nullable=False)

    group_id = Column(Integer(), ForeignKey("group.id"))
    group = relationship('Group', backref="class_time")
    class_room_id = Column(Integer(), ForeignKey('class_room.id'))
    class_room = relationship('ClassRoom', backref="class_time")


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


def main():
    # #Создаем объект Engine, который будет использоваться объектами ниже для связи с БД
    # engine = create_engine('postgresql+psycopg2://postgres:Rufat2001@localhost/testdb')
    
    # #Метод create_all создает таблицы в БД , определенные с помощью  DeclarativeBase
    # DeclarativeBase.metadata.create_all(engine)
    
    # # Создаем фабрику для создания экземпляров Session. Для создания фабрики в аргументе 
    # # bind передаем объект engine
    # Session = sessionmaker(bind=engine)
    
    # # Создаем объект сессии из вышесозданной фабрики Session
    # session = Session()

    #Создаем новую запись.
    
    # Добавляем запись
    # session.drop_all()
    # session.commit()

    # teacher_1 = Teacher(
    #     first_name='Алия',
    #     last_name='Кочербаева',
    #     email=None,
    #     town='Ставрополь',
    #     description='-'
    #     )
    
    # session.add(teacher_1)

    # #Благодаря этой строчке мы добавляем данные а таблицу
    # session.commit()
    
    #А теперь попробуем вывести все посты , которые есть в нашей таблице
    for teacher in session.query(Group):
        print(teacher)
    pass

if __name__ == '__main__':
    main()