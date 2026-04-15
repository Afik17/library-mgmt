from mongoengine import DateField, Document, StringField, IntField


class BookDoc(Document):
    book_id = StringField(unique=True, required=True)
    title = StringField(required=True)
    author = StringField(required=True)
    isbn = StringField(required=True)
    category = StringField(required=True)
    description = StringField(required=True)
    language = StringField(required=True)
    publish_date = DateField(required=True)
    status = StringField(required=True)
