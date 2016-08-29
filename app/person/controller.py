from flask_restful import Resource
from app import api,db
from model import Person
from datetime import datetime
from flask_restful import reqparse


def parse_date(value):
  # ensure the value exists. If not raise error
    if value:
        # parse date and return it
        date_of_birth = datetime.strptime(value, '%m/%d/%Y').date()
        return date_of_birth
    else:
        raise ValueError("Date of Birth cannot be blank!")

# init a new person parser and update person parser
new_person_parser = reqparse.RequestParser(bundle_errors=True)
update_person_parser = reqparse.RequestParser(bundle_errors=True)

#Add arguments for new person parser
new_person_parser.add_argument('firstName', required=True, help="First name cannot be blank!")
new_person_parser.add_argument('lastName', required=True, help="Last name cannot be blank!")
new_person_parser.add_argument('dateOfBirth', type=parse_date, required=True)
new_person_parser.add_argument('zipCode', required=True, help="Zip Code cannot be blank!")

#Add arguments for update person parser
update_person_parser.add_argument('firstName')
update_person_parser.add_argument('lastName')
update_person_parser.add_argument('dateOfBirth', type=parse_date)
update_person_parser.add_argument('zipCode')

# class that will handle Individual people. ie. routes with an id
class PersonRoutes(Resource):
    def get(self,id):
        person = Person.query.get(id)
        if not person:
          return {"message":"Person does not exist with id: " + id }, 405
        else:
          return person.serialize()

    def put(self,id):
        person = Person.query.get(id)
        if not person:
          return {"message":"Person does not exist with id: " + id }, 405
        else:
          args = update_person_parser.parse_args()

          # check to make sure each property exists before updating it
          if args['firstName']:
            person.first_name = args['firstName']

          if args['lastName']:
            person.last_name = args['lastName']

          if args['dateOfBirth']:
            person.date_of_birth = args['dateOfBirth']

          if args['zipCode']:
            person.zip_code = args['zipCode']

          # try to update user
          try:
              db.session.add(person)
              db.session.commit()
              return person.serialize()
          except Exception as e:
              return {"message": "Unknown error occured while adding new user"}

    def delete(self,id):
        person = Person.query.get(id)
        if not person:
          return {"message":"Person does not exist with id: " + id }, 405
        else:
          db.session.delete(person)
          db.session.commit()
          return {}

# class that will handle people routes ie. routes without an id
class PeopleRoutes(Resource):
    def get(self):
      # get all people in DB
        people = Person.query.all()

        # return array of serialized people
        people_json=[i.serialize() for i in people]
        return people_json

    def post(self):
        # parse passed in data
        args = new_person_parser.parse_args()

        # create new person with passed in data
        new_person = Person(args['firstName'], args['lastName'],args['dateOfBirth'] , args['zipCode'])

        # try to add new user to DB
        try:
            db.session.add(new_person)
            db.session.commit()
            return new_person.serialize()
        except Exception as e:
            return {"message": "Unknown error occured while adding new user"}

# add our poeple classes to Router
api.add_resource(PersonRoutes, '/api/person/<id>')
api.add_resource(PeopleRoutes, '/api/person')