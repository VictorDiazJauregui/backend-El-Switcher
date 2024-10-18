import pytest
from app.db.db import CardMove, MoveType
from app.services import cards
from .db_setup import (
    client,
    TestingSessionLocal,
    create_player
)

@pytest.fixture(scope="module")
def test_client():
    yield client

def test_add_cards_to_db():
    db = TestingSessionLocal()
    try:
        cards.add_cards_to_db(999, db)
    except Exception as e:
        assert str(e) == "Game does not exist."


def test_fetch_movement_cards_no_cards():
    db = TestingSessionLocal()
    # Create a player
    player = create_player(db, 1)
    # Fetch movement cards for the player
    result = cards.fetch_movement_cards(player.id, db)

    # Assert that the result is an empty list
    assert result == []

def test_fetch_movement_cards_with_cards():
    db = TestingSessionLocal()
    # Create a player
    player = create_player(db, 1)

    # Add some movement cards to the player
    card1 = CardMove(id=1, game_id=1, owner_id=player.id, move=MoveType.MOV_1)
    card2 = CardMove(id=2, game_id=1, owner_id=player.id, move=MoveType.MOV_2)
    db.add_all([card1, card2])
    db.commit()

    # Fetch movement cards for the player
    result = cards.fetch_movement_cards(player.id, db)

    # Assert that the result contains the correct cards
    assert len(result) == 2
    assert result[0]['movementcardId'] == 1
    assert result[0]['type'] == 'CRUCE DIAGONAL CON UN ESPACIO'
    assert result[0]['moveType'] == 1
    assert result[1]['movementcardId'] == 2
    assert result[1]['type'] == 'CRUCE EN LINEA CON UN ESPACIO'
    assert result[1]['moveType'] == 2