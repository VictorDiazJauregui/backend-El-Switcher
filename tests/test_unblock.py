import pytest
from app.db.db import CardFig, FigureType
from app.schemas.figures import FigureSchema
from app.services import cards
from .db_setup import client, TestingSessionLocal, create_player, reset_db
from app.services.cards import unblock_card


@pytest.fixture(scope="module")
def test_client():
    yield client


def test_unblock_card():
    db = TestingSessionLocal()
    reset_db()

    player1 = create_player(db, 1)
    # Add some figure cards to the players
    card1 = CardFig(
        id=1,
        game_id=1,
        owner_id=player1.id,
        figure=FigureType.EASY_1,
        in_hand=True,
    )
    card2 = CardFig(
        id=2,
        game_id=1,
        owner_id=player1.id,
        figure=FigureType.HARD_1,
        in_hand=True,
    )
    card3 = CardFig(
        id=3,
        game_id=1,
        owner_id=player1.id,
        figure=FigureType.HARD_1,
        in_hand=True,
        block=True,
    )
    db.add_all([card1, card2, card3])
    db.commit()

    unblock_card(player1.id, db)
    assert card3.block == True

    db.delete(card2)
    db.delete(card1)
    db.commit()

    unblock_card(player1.id, db)
    assert card3.block == False
