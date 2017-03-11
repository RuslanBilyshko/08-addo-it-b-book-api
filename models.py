import peewee as pw

db = pw.SqliteDatabase('database.db')


def initialize():
    Book.create_table(fail_silently=True)
    Author.create_table(fail_silently=True)

    try:

        Author.create(
            id=1,
            name="J. K. Rowling"
        )

        Book.create(
            id=1,
            name='Harry Potter',
            author=1
        )

    except pw.IntegrityError:
        pass


class BaseModel(pw.Model):
    class Meta:
        database = db


class Author(BaseModel):
    name = pw.CharField(max_length=100, unique=True)


class Book(BaseModel):
    name = pw.CharField(max_length=100)
    author = pw.ForeignKeyField(Author)
