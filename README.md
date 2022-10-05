# SQLAlchemy Validations

## Learning Goals

After this lesson, you should be able to:

- Explain the purpose of validation
- Add custom validation errors

***

## Key Vocab

- **Validation**: Validation is an automatic check to ensure that data entered is sensible and feasible.

***

## Context: Databases and Data Validity

What is a "validation"?

In the context of Python, **validations** are special method calls that go at the top
of model class definitions and prevent them from being saved to the database if
their data doesn't look right.

In general, **validations** consist of code that performs the job of protecting
the database from invalid data.

SQLAlchemy can validate our models for us before they even touch the database.
This means it's harder to end up with bad data, which can cause problems later
even if our code is technically bug-free.

We can use `SQLAlchemy` helper methods like `validates()` to set things
up.

### SQLAlchemy Validations vs Database Constraints

Many relational databases, such as SQLite and PostgreSQL, have data validation
features that check things like length and data type. While SQLAlchemy
validations are added in the model files, these validations are typically added
via migrations.

Database constraints and model validations are also functionally different.
Database constraints will ALWAYS be checked when adding or updating data in the
database, while SQLAlchemy validations will only be checked when adding or
updating data through the SQLAlchemy ORM (e.g. if we use SQL code in the command line to
modify the database, SQLAlchemy validations are not run).

Some developers use both database constraints and SQLAlchemy Validations,
while others rely on SQLAlchemy Validations alone. Ultimately, it depends on
how the developer plans to add and update data in the database. In this lesson,
we'll be focusing on SQLAlchemy Validations.

### What is "invalid data"?

Suppose you get a new phone and you ask all of your friends for their phone
number again. One of them tells you, "555-868-902". If you're paying attention,
you'll probably wrinkle your nose and think, "Wait a minute. That doesn't sound
like a real phone number."

"555-868-902" is an example of **invalid data**... for a phone number. It's
probably a valid account number for some internet service provider in Alaska,
but there's no way to figure out what your friend's phone number is from those
nine numbers. It's a showstopper, and even worse, it kind of looks like valid
data if you're not looking closely.

### Validations Protect the Database

Invalid data is the bogeyman of web applications: it hides in your database
until the worst possible moment, then jumps out and ruins everything by causing
confusing errors.

Imagine the phone number above being saved to the database in an application
that makes automatic calls using the Twilio API. When your system tries to call
this number, there will be an error because no such phone number exists, which
means you need to have an entire branch of code dedicated to handling _just_
that edge case.

It would be much easier if you never have bad data in the first place, so you
can focus on handling edge cases that are truly unpredictable.

That's where validations come in.

***

## Basic Usage

For more examples of basic validation usage, see the SQLAlchemy Guide for
[SQLAlchemy Validations][SQLAlchemy Validations].

```py
from sqlalchemy.orm import validates

class EmailAddress(Base):
    __tablename__ = 'address'

    id = Column(Integer, primary_key=True)
    email = Column(String)

    @validates('email')
    def validate_email(self, key, address):
        if '@' not in address:
            raise ValueError("failed simple email validation")
        return address



# email = EmailAddress(email='banana')
# session.add(email)
# ValueError: failed simple email validation
```

In this example, we wrote a `validate_email()` function, preventing the object from being saved if its
`email` attribute does not include `@`. We can return a custom message by raising a ValueError with the message.

`validates` is our Swiss Army knife for validations. First you need to use a decorator which takes a string of the columns you want to validate.
the first argument is the **key** we want to validate (the key's value will be the 'email'), and the second argument is the value of what we want to validate.
We can validate multiple columns if we pass multiple column names into the validates decorator.

Here is an example of validating multiple columns with one validate function.

```py
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
```

In this example the `validate_email` function will validate both `email` and the `backup_email` column. We can figure out which column we are validating by
checking the `key` attribute. The key attribute will be `email` or `backup_email` because those are the columns we passed into the decorator.

## Conclusion

In this lesson, we learned the importance of validating data to ensure that no
bad data ends up in our database. We also discussed the difference between model
validations and database constraints. Finally, we saw some common methods for
implementing validations on our models using SQLAlchemy.

***

## Complete code

```py
import sqlalchemy

from sqlalchemy import CheckConstraint
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import validates


connection_string = "sqlite:///database.db"   # for SQLite, local file
db   = create_engine(connection_string)
base = declarative_base()

from sqlalchemy.orm import validates

class EmailAddress(base):
    __tablename__ = 'address'

    id = Column(Integer, primary_key=True)
    email = Column(String)

    @validates('email')
    def validate_email(self, key, address):
        if '@' not in address:
            raise ValueError("failed simple email validation")
        return address

Session = sessionmaker(db)
session = Session()

base.metadata.create_all(db)

email = EmailAddress(email='banana')
session.add(email)

try:
    session.commit()
except sqlalchemy.exc.IntegrityError as e:
    print("Integrity violation blocked!")
    session.rollback()

```

***

## Resources

- [SQLAlchemy Validations][SQLAlchemy Validations]

[SQLAlchemy Validations]: https://docs.sqlalchemy.org/en/14/orm/mapped_attributes.html
