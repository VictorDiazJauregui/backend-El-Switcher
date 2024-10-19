import pytest
import numpy as np

from app.models.figures import Figure, get_all_figures
from app.db.db import GameStatus
from .db_setup import (
    client,
    TestingSessionLocal,
    create_game,
    add_example_board,
)


@pytest.fixture(scope="module")
def test_client():
    yield client


def test_to_binary():
    fig = Figure("test", np.array([[1, 2], [None, 4]]))
    binary_matrix = fig._to_binary(fig.matrix_figure)
    expected_matrix = np.array([[1, 1], [0, 1]])
    np.testing.assert_array_equal(binary_matrix, expected_matrix)


def test_get_all_rotations():
    fig = Figure("test", np.array([[1, 2], [3, 4]]))
    rotations = fig.get_all_rotations()
    expected_rotations = [
        np.array([[1, 2], [3, 4]]),
        np.array([[2, 4], [1, 3]]),
        np.array([[4, 3], [2, 1]]),
        np.array([[3, 1], [4, 2]]),
    ]
    for rotation, expected in zip(rotations, expected_rotations):
        np.testing.assert_array_equal(rotation, expected)


def test_matches_any_rotation():
    fig = Figure("test", np.array([[1, 2], [3, 4]]))
    connected_component = np.array([[4, 3], [2, 1]])
    assert fig.matches_any_rotation(connected_component)

    connected_component = np.array([[1, 2], [3, None]])
    assert not fig.matches_any_rotation(connected_component)


def test_figures():
    figures = get_all_figures()
    len(figures) == 19
    for fig in figures:
        assert isinstance(fig, Figure)
        assert hasattr(fig, "type_name")
        assert hasattr(fig, "matrix_figure")


def test_figures_success():
    db = TestingSessionLocal()
    game = create_game(db, GameStatus.LOBBY)
    add_example_board(db, game.id)

    response = client.get(f"/game/{game.id}/figures")

    assert response.status_code == 200
    print(response.json())


def test_board_not_found():

    fake_id = 999

    response = client.get(f"/game/{fake_id}/figures")

    assert response.status_code == 404
    assert (
        response.json()["detail"]
        == f"Board for game {fake_id} does not exist."
    )
