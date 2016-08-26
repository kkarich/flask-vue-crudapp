from app import db

class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    date_of_birth = db.Column(db.Date())
    zip_code = db.Column(db.String(10))

    def __init__(self, first_name, last_name, date_of_birth, zip_code):
        self.first_name = first_name
        self.last_name = last_name
        self.date_of_birth = date_of_birth
        self.zip_code = zip_code


    def serialize(self):
        # Return object data in easily serializeable format
        return {
            'id' : self.id,
            'firstName' : self.first_name,
            'lastName' : self.last_name,
            'dateOfBirth': dump_datetime(self.date_of_birth),
            'zipCode' : self.zip_code,
            }

    def __repr__(self):
        return 'Name: ' + self.first_name + ' ' + self.last_name


def dump_datetime(value):
    # Deserialize datetime object into string form for JSON processing.
    if value is None:
        return None
    return value.strftime("%m/%d/%Y")