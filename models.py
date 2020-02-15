from sqlalchemy import Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.sqlite import DATETIME, INTEGER, TEXT

Base = declarative_base()

class Houses(Base):
    __tablename__ = 'houses'
    __table_args__ = {'sqlite_autoincrement': True}
    id = Column(INTEGER, primary_key=True, nullable=False)
    street = Column(TEXT)
    region = Column(TEXT)
    rooms = Column(INTEGER, nullable=False)
    area = Column(INTEGER)
    rent = Column(INTEGER, nullable=False)
    story = Column(INTEGER)
    applicants = Column(INTEGER)
    points = Column(INTEGER, nullable=False)
    built = Column(INTEGER)
    renovated = Column(INTEGER)
    last_app = Column(DATETIME)
    date_added = Column(DATETIME)