from utils.data_generator import DataGenerator

# ---------- POSITIVE ----------



def test_get_movies(api_manager):
    response = api_manager.movies_api.get_movies()
    response_data = response.json()

    assert isinstance(response_data["movies"], list)
    assert isinstance(response_data["count"], int)
    assert isinstance(response_data["pageSize"], int)


def test_create_movie(authenticated_api_manager, movie_data):
    response = authenticated_api_manager.movies_api.create_movie(movie_data)
    response_data = response.json()

    try:
        assert "id" in response_data
        assert response_data["name"] == movie_data["name"]
        assert response_data["price"] == movie_data["price"]
    finally:
        authenticated_api_manager.movies_api.delete_movie(
            response_data["id"]
        )


def test_get_movie_by_id(api_manager, created_movie):
    movie_id = created_movie["id"]

    response = api_manager.movies_api.get_movie_by_id(movie_id)
    response_data = response.json()

    assert response_data["id"] == movie_id
    assert response_data["name"] == created_movie["name"]
    assert response_data["price"] == created_movie["price"]


def test_update_movie(authenticated_api_manager, created_movie):
    movie_id = created_movie["id"]
    update_data = DataGenerator.generate_movie_data()

    authenticated_api_manager.movies_api.update_movie(
        movie_id,
        update_data,
    )

    get_response = authenticated_api_manager.movies_api.get_movie_by_id(
        movie_id
    )
    response_data = get_response.json()

    assert response_data["id"] == movie_id
    assert response_data["name"] == update_data["name"]
    assert response_data["price"] == update_data["price"]


def test_delete_movie(authenticated_api_manager, movie_data):
    create_response = authenticated_api_manager.movies_api.create_movie(
        movie_data
    )
    created_movie = create_response.json()
    movie_id = created_movie["id"]

    delete_response = authenticated_api_manager.movies_api.delete_movie(
        movie_id
    )
    delete_data = delete_response.json()

    get_response = authenticated_api_manager.movies_api.get_movie_by_id(
        movie_id,
        expected_status=404,
    )

    assert delete_data["id"] == movie_id
    assert delete_data["name"] == movie_data["name"]
    assert get_response.status_code == 404


def test_filter_movies_by_location(api_manager):
    location = "MSK"

    response = api_manager.movies_api.get_movies(
        params={"locations": location}
    )
    response_data = response.json()

    assert isinstance(response_data["movies"], list)
    assert len(response_data["movies"]) > 0
    assert all(
        movie["location"] == location
        for movie in response_data["movies"]
    )


# ---------- NEGATIVE ----------

def test_get_nonexistent_movie(api_manager):
    nonexistent_movie_id = -1

    response = api_manager.movies_api.get_movie_by_id(
        nonexistent_movie_id,
        expected_status=404,
    )

    assert response.status_code == 404


def test_create_movie_without_name(
    authenticated_api_manager,
    movie_data,
):
    movie_data.pop("name")

    response = authenticated_api_manager.movies_api.create_movie(
        movie_data,
        expected_status=400,
    )

    assert response.status_code == 400


def test_create_duplicate_movie(
    authenticated_api_manager,
    movie_data,
):
    first_response = authenticated_api_manager.movies_api.create_movie(
        movie_data
    )
    created_movie = first_response.json()

    try:
        duplicate_response = (
            authenticated_api_manager.movies_api.create_movie(
                movie_data,
                expected_status=409,
            )
        )

        assert duplicate_response.status_code == 409

    finally:
        authenticated_api_manager.movies_api.delete_movie(
            created_movie["id"]
        )


def test_create_movie_without_permissions(
    user_api_manager,
    movie_data,
):
    response = user_api_manager.movies_api.create_movie(
        movie_data,
        expected_status=403,
    )

    assert response.status_code == 403





