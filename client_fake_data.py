from app import app, db, Client

from faker import Faker

with app.app_context():
    fake = Faker()

    for i in range(10):
        item = Client(
            company=fake.company(),
            street=fake.street_address(),
            suburb=fake.city(),
            contact_person=fake.name(),
            contact_number=fake.phone_number(),
            email=fake.email(),
        )
        db.session.add(item)
        db.session.commit()