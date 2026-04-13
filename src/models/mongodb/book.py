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
    total_copies = IntField(required=True, min_value=0)
    available_copies = IntField(required=True, min_value=0)
