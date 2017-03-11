from marshmallow import ValidationError
from marshmallow import fields, validate, validates
from marshmallow_peewee import ModelSchema
from models import Author, Book
from marshmallow_peewee import Related


class AuthorSchema(ModelSchema):
    name = fields.Str(validate=[validate.Length(min=3, max=50)])

    class Meta:
        model = Author


class BookSchema(ModelSchema):
    name = fields.Str(validate=[validate.Length(min=3, max=100)])
    author = Related(nested=AuthorSchema)

    class Meta:
        model = Book

    @validates('author')
    def validate_author(self, value):
        if not Author.filter(Author.id == value).exists():
            raise ValidationError("Can't find author")


author_schema = AuthorSchema()
book_schema = BookSchema()
