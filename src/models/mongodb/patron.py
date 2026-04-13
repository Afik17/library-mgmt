from mongoengine import Document, StringField, DateField, FloatField


class PatronDoc(Document):
    patron_id = StringField(unique=True, required=True)
    first_name = StringField(required=True)
    last_name = StringField(required=True)
    email = StringField(required=True)
    phone_number = StringField(required=True)
    birth_date = DateField(required=True)
    membership_date = DateField(required=True)
    role = StringField(required=True)
    status = StringField(required=True)
    monthly_payment = FloatField(required=True, min_value=0)
    discount_rate = FloatField(required=True, max_value=100, min_value=0)
