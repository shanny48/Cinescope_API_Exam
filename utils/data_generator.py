from faker import Faker
import random


class DataGenerator:
    faker = Faker()

    @classmethod
    def generate_random_email(cls):
        return cls.faker.unique.email()

    @classmethod
    def generate_random_name(cls):
        return cls.faker.name()

    @classmethod
    def generate_random_password(cls):
        return "Test12345Q"

    @classmethod
    def generate_movie_data(cls):
        return {
            "name": f"{cls.faker.word().capitalize()}-{cls.faker.uuid4()[:8]}",
            "imageUrl": cls.faker.image_url(),
            "price": random.randint(100, 900),
            "description": cls.faker.sentence(),
            "location": random.choice(["MSK", "SPB"]),
            "published": True,
            "genreId": 1,
        }