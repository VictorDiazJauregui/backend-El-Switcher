import pytest
from unittest.mock import MagicMock, patch, AsyncMock
from fastapi.testclient import TestClient

from app.main import app
from app.db.db import GameStatus, Turn, CardFig, Color
from app.models.figures import get_figure_type_by_id
from app.schemas.figures import FigureSchema
from app.services.validate_figure import validate, select_figure_by_his_type
from .db_setup import (
    TestingSessionLocal,
    create_game,
    create_player,
    create_card_fig,
    create_figure,
    add_example_board,
)

# pytestmark = pytest.mark.skip(reason="Tests deshabilitados en este módulo")


@pytest.fixture
def test_client():
    return TestClient(app)


@pytest.fixture
def db_session():
    db = TestingSessionLocal()
    yield db
    db.close()


@pytest.fixture
def figures_info():
    return FigureSchema(
        colorCards=[
            {"row": 0, "column": 0, "color": Color.RED},
            {"row": 0, "column": 1, "color": Color.RED},
        ],
        figureCardId=998,
    )


@pytest.fixture
def not_found_figure_info():
    return FigureSchema(
        colorCards=[
            {"row": 0, "column": 0, "color": Color.RED},
            {"row": 0, "column": 1, "color": Color.RED},
        ],
        figureCardId=999,
    )


def test_get_figure_type_by_id(db_session):
    db_session.add(CardFig(id=995, figure="EASY_7"))
    db_session.commit()

    figure_type = get_figure_type_by_id(995, db_session)
    assert figure_type.name == "EASY_7"
    assert figure_type.value[1] == "Figura Fácil 7"


@patch("app.services.game_events.emit_block_color", new_callable=AsyncMock)
@patch("app.services.validate_figure.set_block_color")
@patch("app.services.validate_figure.figure_checks")
@patch("app.services.validate_figure.board_checks")
def test_validate_figure_returns_200(
    mock_board_checks,
    mock_figure_checks,
    mock_set_block_color,
    mock_emit_block_color,
    db_session,
    test_client,
):
    # Create test data
    game = create_game(db_session, GameStatus.INGAME)
    board = add_example_board(db_session, game.id)
    player = create_player(db_session, game.id)
    card = create_card_fig(db_session, game.id, player.id)
    figure = create_figure(card.id)

    # Mock the figure lookups
    mock_board_checks.return_value = None
    mock_figure_checks.return_value = None
    mock_set_block_color.return_value = None
    mock_emit_block_color.return_value = None

    response = test_client.post(
        f"/game/{game.id}/play_figure/{player.id}", json=figure.model_dump()
    )
    print(response.json())

    assert response.status_code == 200


def test_validate_figure_game_not_found(db_session, figures_info):
    with pytest.raises(ValueError, match="Game not found"):
        validate(figures_info, 999, 1, db_session)


def test_validate_figure_player_not_found(db_session, figures_info):
    game = create_game(db_session, GameStatus.INGAME)

    with pytest.raises(ValueError, match="Player not found"):
        validate(figures_info, game.id, 999, db_session)


def test_player_checks_player_not_belong_to_game(db_session):
    game1 = create_game(db_session, GameStatus.INGAME)
    game2 = create_game(db_session, GameStatus.INGAME)
    player = create_player(db_session, game2.id)

    with pytest.raises(ValueError, match="Player does not belong to game"):
        validate(figures_info, game1.id, player.id, db_session)


def test_validate_figure_not_your_turn(db_session, figures_info):
    game = create_game(db_session, GameStatus.INGAME)
    player = create_player(db_session, game.id)
    game.turn = Turn.P3
    db_session.commit()

    with pytest.raises(ValueError, match="Not your turn"):
        validate(figures_info, game.id, player.id, db_session)


def test_validate_figure_game_not_in_progress(db_session, figures_info):
    game = create_game(db_session, GameStatus.FINISHED)
    player = create_player(db_session, game.id)

    with pytest.raises(ValueError, match="Game is not in progress"):
        validate(figures_info, game.id, player.id, db_session)


@patch("app.services.validate_figure.get_figure_by_id")
@patch("app.services.validate_figure.get_figure_type_by_id")
@patch("app.services.validate_figure.find_connected_components")
@patch("app.services.validate_figure.board_checks")
def test_validate_figure_no_connected_components(
    mock_board_checks,
    mock_find_connected_components,
    mock_get_figure_type_by_id,
    mock_get_figure_by_id,
    db_session,
    figures_info,
):
    game = create_game(db_session, GameStatus.INGAME)
    player = create_player(db_session, game.id)

    mock_board_checks.return_value = None

    # Set up proper mock returns
    mock_figure = MagicMock()
    mock_figure_type = MagicMock()

    mock_get_figure_by_id.return_value = mock_figure
    mock_get_figure_type_by_id.return_value = mock_figure_type
    mock_find_connected_components.return_value = []  # Mock returns None

    with pytest.raises(ValueError, match="No connected components found"):
        validate(figures_info, game.id, player.id, db_session)


@patch("app.services.validate_figure.get_figure_by_id")
@patch("app.services.validate_figure.get_figure_type_by_id")
@patch("app.services.validate_figure.find_connected_components")
@patch("app.services.validate_figure.board_checks")
def test_validate_figure_more_than_one_connected_component(
    mock_board_checks,
    mock_find_connected_components,
    mock_get_figure_type_by_id,
    mock_get_figure_by_id,
    db_session,
    figures_info,
):
    game = create_game(db_session, GameStatus.INGAME)
    player = create_player(db_session, game.id)

    mock_board_checks.return_value = None

    # Set up proper mock returns
    mock_figure = MagicMock()
    mock_figure_type = MagicMock()

    mock_get_figure_by_id.return_value = mock_figure
    mock_get_figure_type_by_id.return_value = mock_figure_type
    mock_find_connected_components.return_value = [
        "lol",
        "lmao",
    ]  # More than one connected "component"

    with pytest.raises(
        ValueError, match="More than one connected component found"
    ):
        validate(figures_info, game.id, player.id, db_session)


@patch("app.services.validate_figure.board_checks")
def test_validate_figure_figure_not_found(
    mock_board_checks, db_session, not_found_figure_info
):

    game = create_game(db_session, GameStatus.INGAME)
    player = create_player(db_session, game.id)

    mock_board_checks.return_value = None

    with pytest.raises(ValueError, match="Figure not found"):
        validate(not_found_figure_info, game.id, player.id, db_session)


@patch("app.services.game_events.emit_block_color", new_callable=AsyncMock)
@patch("app.services.validate_figure.set_block_color")
@patch("app.services.validate_figure.figure_checks")
@patch("app.services.validate_figure.board_checks")
def test_validate_figure_returns_200(
    mock_board_checks,
    mock_figure_checks,
    mock_set_block_color,
    mock_emit_block_color,
    db_session,
    test_client,
):
    # Create test data
    game = create_game(db_session, GameStatus.INGAME)
    board = add_example_board(db_session, game.id)
    player = create_player(db_session, game.id)
    card = create_card_fig(db_session, game.id, player.id)
    figure = create_figure(card.id)

    # Mock the figure lookups
    mock_board_checks.return_value = None
    mock_figure_checks.return_value = None
    mock_set_block_color.return_value = None
    mock_emit_block_color.return_value = None


@patch("app.services.validate_figure.get_figure_by_id")
@patch("app.services.validate_figure.get_figure_type_by_id")
@patch("app.services.validate_figure.board_checks")
def test_validate_figure_figure_type_not_found(
    mock_board_checks,
    mock_get_figure_type_by_id,
    mock_get_figure_by_id,
    db_session,
    not_found_figure_info,
):
    game = create_game(db_session, GameStatus.INGAME)
    player = create_player(db_session, game.id)

    mock_board_checks.return_value = None

    # Create a mock figure with a valid game_id
    mock_figure = MagicMock()
    mock_figure.game_id = game.id
    mock_get_figure_by_id.return_value = mock_figure

    mock_get_figure_type_by_id.return_value = None

    with pytest.raises(ValueError, match="Figure type not found"):
        validate(not_found_figure_info, game.id, player.id, db_session)


@patch("app.services.validate_figure.get_figure_by_id")
@patch("app.services.validate_figure.get_figure_type_by_id")
@patch("app.services.validate_figure.select_figure_by_his_type")
@patch("app.services.validate_figure.board_checks")
def test_validate_figure_figure_does_not_match(
    mock_board_checks,
    mock_select_figure_by_his_type,
    mock_get_figure_type_by_id,
    mock_get_figure_by_id,
    db_session,
    figures_info,
):
    game = create_game(db_session, GameStatus.INGAME)
    player = create_player(db_session, game.id)

    mock_board_checks.return_value = None

    # Create a mock figure with a valid game_id
    mock_figure = MagicMock()
    mock_figure.game_id = game.id
    mock_get_figure_by_id.return_value = mock_figure

    mock_get_figure_type_by_id.return_value = MagicMock()
    mock_select_figure_by_his_type.return_value.matches_any_rotation.return_value = (
        False
    )

    with pytest.raises(
        ValueError, match="Figure does not match connected component"
    ):
        validate(figures_info, game.id, player.id, db_session)


FIGURE_TYPE_CASES = {
    "Figura Difícil 1": 1,
    "Figura Difícil 2": 2,
    "Figura Difícil 3": 3,
    "Figura Difícil 4": 4,
    "Figura Difícil 5": 5,
    "Figura Difícil 6": 6,
    "Figura Difícil 7": 7,
    "Figura Difícil 8": 8,
    "Figura Difícil 9": 9,
    "Figura Difícil 10": 10,
    "Figura Difícil 11": 11,
    "Figura Difícil 12": 12,
    "Figura Difícil 13": 13,
    "Figura Difícil 14": 14,
    "Figura Difícil 15": 15,
    "Figura Difícil 16": 16,
    "Figura Difícil 17": 17,
    "Figura Difícil 18": 18,
    "Figura Fácil 4": 19,
    "Figura Fácil 1": 20,
    "Figura Fácil 2": 21,
    "Figura Fácil 3": 22,
    "Figura Fácil 5": 23,
    "Figura Fácil 6": 24,
    "Figura Fácil 7": 25,
}


@pytest.mark.parametrize("figure_type,figure_id", FIGURE_TYPE_CASES.items())
@patch("app.services.game_events.emit_block_color", new_callable=AsyncMock)
@patch("app.services.validate_figure.set_block_color")
@patch("app.services.validate_figure.board_checks")
@patch("app.services.validate_figure.get_figure_by_id")
@patch("app.services.validate_figure.get_figure_type_by_id")
@patch("app.services.validate_figure.find_connected_components")
def test_validate_figure_all_types(
    mock_find_connected_components,
    mock_get_figure_type_by_id,
    mock_get_figure_by_id,
    mock_board_checks,
    mock_set_block_color,
    mock_emit_block_color,
    figure_type,
    figure_id,
    db_session,
    figures_info,
):  # Use the fixture we already have
    # Create test data
    game = create_game(db_session, GameStatus.INGAME)
    player = create_player(db_session, game.id)

    # Mock the figure lookups
    mock_board_checks.return_value = None
    mock_set_block_color.return_value = None
    mock_emit_block_color.return_value = None

    # Mock the figure lookups
    mock_figure = MagicMock()
    mock_figure.game_id = game.id
    mock_get_figure_by_id.return_value = mock_figure

    mock_figure_type = MagicMock()
    mock_figure_type.value = (figure_id, figure_type)
    mock_get_figure_type_by_id.return_value = mock_figure_type

    # Get the actual figure instance
    figure = select_figure_by_his_type(figure_type)
    assert figure is not None, f"Figure {figure_type} should not be None"
    assert (
        figure.type_name == figure_type
    ), f"Figure type mismatch: expected {figure_type}, got {figure.type_name}"
    assert hasattr(
        figure, "matrix_figure"
    ), f"Figure {figure_type} missing matrix_figure attribute"

    # Mock connected components to return a matching component
    mock_find_connected_components.return_value = [figure.matrix_figure]

    # Call the function and verify it returns 200
    result = validate(figures_info, game.id, player.id, db_session)
    assert result == 200


def test_select_figure_by_his_type_none():
    # Test cases for None return
    invalid_types = [
        None,
        "",
        "Invalid Figure",
        "Figura Inexistente",
        "Figura Difícil 99",
        "Figura Fácil 99",
    ]

    for invalid_type in invalid_types:
        figure = select_figure_by_his_type(invalid_type)
        assert (
            figure is None
        ), f"Expected None for invalid type: {invalid_type}"


@patch("app.services.game_events.emit_cards")
@patch("app.services.cards.unassign_played_movement_cards")
@patch("app.services.cards.delete_figure_card")
@patch("app.services.board.delete_partial_cache")
@patch("app.services.validate_figure.validate")
@patch("app.services.validate_figure.board_checks")
def test_validate_figure_failure(
    mock_board_checks,
    mock_validate_figure,
    mock_delete_partial_cache,
    mock_delete_figure_card,
    mock_unassign_played_movement_cards,
    mock_emit_cards,
    test_client,
):

    db = TestingSessionLocal()
    game = create_game(db, GameStatus.INGAME)
    player = create_player(db, game.id)
    card = create_card_fig(db, game.id, player.id)

    mock_board_checks.return_value = None

    # Mock validate_figure to return error
    mock_validate_figure.return_value = 400

    # Test data
    figure_data = {
        "colorCards": [
            {"row": 0, "column": 0, "color": "Red"},
            {"row": 0, "column": 1, "color": "Red"},
        ],
        "figureCardId": card.id,
    }

    # Make request
    response = test_client.post(
        f"/game/{game.id}/play_figure/{player.id}", json=figure_data
    )

    # Assertions
    assert response.status_code == 400

    # Verify cleanup functions were not called
    mock_delete_partial_cache.assert_not_called()
    mock_delete_figure_card.assert_not_called()
    mock_unassign_played_movement_cards.assert_not_called()
    mock_emit_cards.assert_not_called()
