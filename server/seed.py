#!/usr/bin/env python3

from random import choice as rc

from faker import Faker

from app import app
from models import db, EmailAddress

# db.init_app(app)

fake = Faker()

with app.app_context():

    EmailAddress.query.delete()

    emails = []
    for n in range(25):
        em = EmailAddress(email='email@email.com', backup_email = 'email@email.com')
        emails.append(em)

    db.session.add_all(emails)


    db.session.commit()
