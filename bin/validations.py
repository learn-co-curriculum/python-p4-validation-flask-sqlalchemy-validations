import sqlalchemy

from sqlalchemy import CheckConstraint
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import validates


connection = "sqlite:///database.db" 
db   = create_engine(connection)
base = declarative_base()

class EmailAddress(base):
    __tablename__ = 'address'

    id = Column(Integer, primary_key=True)
    email = Column(String)
    backup_email = Column(String)

    @validates('email', 'backup_email')
    def validate_email(self, key, address):
        
        if '@' not in address:
            raise ValueError("failed simple email validation")
        return address

Session = sessionmaker(db)
session = Session()

base.metadata.create_all(db)

email = EmailAddress(email='firstname@student.com', backup_email='firstnameBackup@student.com')
session.add(email)

try:
    session.commit()
except sqlalchemy.exc.IntegrityError as e:
    print("Integrity violation blocked!")
    session.rollback()
