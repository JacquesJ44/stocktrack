from app import db, Item

from faker import Faker

from . import app

with app.app_context():
    fake = Faker()

    for i in range(10):
        item = Item(
            client=fake.company(),
            brand=fake.name(),
            model=fake.color_name(),
            serial=fake.word(),
            problem=fake.text(),
            date_booked=fake.date(),
            etr=fake.date(),
            at_repair_site=fake.boolean()
        )
        db.session.add(item)
        db.session.commit()

