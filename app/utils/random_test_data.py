from faker import Faker

from app.models.User import UserCreate

TEST_DATA_PREFIX = 'autotest_'


def user():
    faker = Faker()

    random_user = {
        'email': f'{TEST_DATA_PREFIX}{faker.email()}',
        'first_name': f'{TEST_DATA_PREFIX}{faker.first_name()}',
        'last_name': f'{TEST_DATA_PREFIX}{faker.last_name()}',
        'avatar': f'{faker.image_url()}',
    }

    UserCreate(**random_user)
    return random_user
