import pytest
import requests

from clients.api_manager import ApiManager
from utils.data_generator import DataGenerator


@pytest.fixture(scope="session")
def session():
    http_session = requests.Session()

    yield http_session

    http_session.close()


@pytest.fixture(scope="session")
def api_manager(session):
    return ApiManager(session)


@pytest.fixture(scope="session")
def authenticated_api_manager(api_manager):
    admin_data = {
        "email": "api1@gmail.com",
        "password": "asdqwe123Q",
    }

    api_manager.auth_api.authenticate(admin_data)

    return api_manager


@pytest.fixture
def movie_data():
    return DataGenerator.generate_movie_data()


@pytest.fixture
def created_movie(authenticated_api_manager, movie_data):
    response = authenticated_api_manager.movies_api.create_movie(
        movie_data
    )

    movie = response.json()

    yield movie

    authenticated_api_manager.movies_api.delete_movie(
        movie["id"]
    )


@pytest.fixture
def user_api_manager():
    user_session = requests.Session()
    api_manager = ApiManager(user_session)

    password = DataGenerator.generate_random_password()

    user_data = {
        "email": DataGenerator.generate_random_email(),
        "fullName": DataGenerator.generate_random_name(),
        "password": password,
        "passwordRepeat": password,
        "roles": ["USER"],
    }

    api_manager.auth_api.register_user(user_data)

    login_data = {
        "email": user_data["email"],
        "password": user_data["password"],
    }

    api_manager.auth_api.authenticate(login_data)

    yield api_manager

    user_session.close()