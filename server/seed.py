from app import db, create_app
from models import UserAuth, Software, SoftwareVersionCheck
from flask_bcrypt import generate_password_hash
from faker import Faker

faker = Faker()

def seed_users(n):
    for _ in range(n):
        hashed_password = generate_password_hash("testpassword").decode('utf-8')
        user = UserAuth(
            username=faker.user_name(),
            email=faker.email(),
            password_hash=hashed_password
        )
        db.session.add(user)
    db.session.commit()

def seed_software(n):
    for _ in range(n):
        software = Software(
            name=faker.company()
        )
        db.session.add(software)
    db.session.commit()

def seed_version_checks(n):
    users = UserAuth.query.all()
    software_list = Software.query.all()
    for _ in range(n):
        user_id = faker.random_int(min=1, max=len(users))
        software_id = faker.random_int(min=1, max=len(software_list))
        version_check = SoftwareVersionCheck(
            user_id=user_id,
            software_id=software_id,
        )
        db.session.add(version_check)
    db.session.commit()

def seed_database():
    db.create_all()

    seed_users(10)
    seed_software(5)
    seed_version_checks(20)

    print("Database seeded successfully!")

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        seed_database()
