from mongoengine import Document, StringField, DateField


class BorrowDoc(Document):
    borrow_id = StringField(unique=True, required=True)
    book_id = StringField(required=True)
    patron_id = StringField(required=True)
    checkout_date = DateField(required=True)
    due_date = DateField(required=True)
    return_date = DateField()
