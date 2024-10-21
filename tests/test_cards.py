import pytest
from app.db.db import CardMove, MoveType, CardFig, FigureType
from app.schemas.figures import FigureSchema
from app.services import cards
from .db_setup import client, TestingSessionLocal, create_player, reset_db


@pytest.fixture(scope="module", autouse=True)
def reset_database_at_end():
    """Fixture to reset the database after all tests in the module."""
    yield
    reset_db()


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
    assert result[0]["movementcardId"] == 1
    assert result[0]["type"] == "CRUCE DIAGONAL CON UN ESPACIO"
    assert result[0]["moveType"] == 1
    assert result[1]["movementcardId"] == 2
    assert result[1]["type"] == "CRUCE EN LINEA CON UN ESPACIO"
    assert result[1]["moveType"] == 2


def test_fetch_figure_cards_with_cards():
    db = TestingSessionLocal()
    reset_db()

    player1 = create_player(db, 1)
    player2 = create_player(db, 1)
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
        owner_id=player2.id,
        figure=FigureType.HARD_1,
        in_hand=True,
    )
    db.add_all([card1, card2])
    db.commit()

    # Fetch figure cards for the player
    result = cards.fetch_figure_cards(game_id=1, db=db)
    print(result)

    # Access cards of the first player
    player1_cards = result[0]["cards"]

    # Assert the expected cards for player1
    assert len(player1_cards) == 1, "Player 1 should have one card."
    assert (
        player1_cards[0]["figureCardId"] == card1.id
    ), f"Expected card ID {card1.id}, got {player1_cards[0]['figureCardId']}."
    assert (
        player1_cards[0]["difficulty"] == "easy"
    ), "Expected difficulty for Player 1's card to be 'easy'."
    assert (
        player1_cards[0]["figureType"] == 1
    ), "Expected figure type for Player 1's card to be 1."

    # Access cards of the second player
    player2_cards = result[1]["cards"]

    # Assert the expected cards for player2
    assert len(player2_cards) == 1, "Player 2 should have one card."
    assert (
        player2_cards[0]["figureCardId"] == card2.id
    ), f"Expected card ID {card2.id}, got {player2_cards[0]['figureCardId']}."
    assert (
        player2_cards[0]["difficulty"] == "hard"
    ), "Expected difficulty for Player 2's card to be 'hard'."
    assert (
        player2_cards[0]["figureType"] == 1
    ), "Expected figure type for Player 2's card to be 1."


### ================================== ASSIGN FIGURE ============================================


def test_assign_figure_cards():
    db = TestingSessionLocal()
    player = create_player(db, 4)

    # ---------------------- ZERO CARDS -------------------------------------------
    cards_in_hand = (
        db.query(CardFig)
        .filter(CardFig.owner_id == player.id, CardFig.in_hand == True)
        .all()
    )
    assert (
        len(cards_in_hand) == 0
    ), "El jugador no deberia tener cartas en la mano."

    # Inicializa algunas cartas disponibles
    available_card1 = CardFig(
        game_id=4, owner_id=player.id, figure=FigureType.EASY_1, in_hand=False
    )
    available_card2 = CardFig(
        game_id=4, owner_id=player.id, figure=FigureType.EASY_2, in_hand=False
    )
    available_card3 = CardFig(
        game_id=4, owner_id=player.id, figure=FigureType.EASY_3, in_hand=False
    )
    db.add_all([available_card1, available_card2, available_card3])
    db.commit()

    # Asigna las cartas
    cards.assign_figure_cards(game_id=4, player_id=player.id, db=db)

    # Verifica que el jugador tenga 3 cartas
    cards_in_hand = (
        db.query(CardFig)
        .filter(CardFig.owner_id == player.id, CardFig.in_hand == True)
        .all()
    )
    assert (
        len(cards_in_hand) == 3
    ), "El jugador debería tener 3 cartas en la mano."

    # ---------------------- FULL HAND --------------------------------------------
    # Inicializa algunas cartas disponibles
    available_card4 = CardFig(
        game_id=4, owner_id=player.id, figure=FigureType.HARD_1, in_hand=False
    )
    available_card5 = CardFig(
        game_id=4, owner_id=player.id, figure=FigureType.EASY_2, in_hand=False
    )
    available_card6 = CardFig(
        game_id=4, owner_id=player.id, figure=FigureType.EASY_4, in_hand=False
    )
    db.add_all([available_card4, available_card5, available_card6])
    db.commit()

    # Intenta asignar cartas cuando la mano del jugador esta llena
    cards.assign_figure_cards(game_id=4, player_id=player.id, db=db)

    # Verifica que el jugador aún tenga 3 cartas
    cards_in_hand = (
        db.query(CardFig)
        .filter(CardFig.owner_id == player.id, CardFig.in_hand == True)
        .all()
    )
    assert (
        len(cards_in_hand) == 3
    ), "El jugador debería seguir teniendo 3 cartas en la mano."

    # ---------------------- ONE SLOT EMPTY ----------------------------------------
    cards.delete_figure_card(available_card1.id, db)
    cards_in_hand = (
        db.query(CardFig)
        .filter(CardFig.owner_id == player.id, CardFig.in_hand == True)
        .all()
    )
    assert (
        len(cards_in_hand) == 2
    ), "El jugador debería tener 2 cartas en la mano."

    cards.assign_figure_cards(game_id=4, player_id=player.id, db=db)

    cards_in_hand = (
        db.query(CardFig)
        .filter(CardFig.owner_id == player.id, CardFig.in_hand == True)
        .all()
    )
    assert (
        len(cards_in_hand) == 3
    ), "El jugador debería tener 3 cartas en la mano."


def test_assign_figure_cards_with_blocked_card():
    db = TestingSessionLocal()
    player = create_player(db, 4)

    # Crea una carta bloqueada
    blocked_card = CardFig(
        game_id=4,
        owner_id=player.id,
        figure=FigureType.HARD_2,
        in_hand=True,
        block=True,
    )
    db.add(blocked_card)
    db.commit()

    # Asigna las cartas
    cards.assign_figure_cards(game_id=4, player_id=player.id, db=db)

    # Verifica que el jugador siga teniendo una carta
    cards_in_hand = (
        db.query(CardFig)
        .filter(CardFig.owner_id == player.id, CardFig.in_hand == True)
        .all()
    )
    assert (
        len(cards_in_hand) == 1
    ), "El jugador debería tener 1 carta en la mano debido a que la carta está bloqueada."


### =============================== ASSIGN MOVEMENT ======================================
### Tests para `assign_movement_cards`
def test_assign_movement_cards_with_empty_hand():
    db = TestingSessionLocal()
    reset_db()

    player = create_player(db, 1)

    # ------------------------------ ZERO CARDS ---------------------------------
    # Inicializa algunas cartas de movimiento disponibles
    available_card1 = CardMove(
        id=1, game_id=1, owner_id=None, move=MoveType.MOV_1, played=False
    )
    available_card2 = CardMove(
        id=2, game_id=1, owner_id=None, move=MoveType.MOV_2, played=False
    )
    available_card3 = CardMove(
        id=3, game_id=1, owner_id=None, move=MoveType.MOV_3, played=False
    )
    db.add_all([available_card1, available_card2, available_card3])
    db.commit()

    # Asigna las cartas de movimiento
    cards.assign_movement_cards(game_id=1, player_id=player.id, db=db)

    # Verifica que el jugador tenga 3 cartas
    cards_in_hand = (
        db.query(CardMove).filter(CardMove.owner_id == player.id).all()
    )
    assert (
        len(cards_in_hand) == 3
    ), "El jugador debería tener 3 cartas de movimiento en la mano."

    # ----------------------------- FULL HAND --------------------------------------
    available_card4 = CardMove(
        id=4, game_id=1, owner_id=None, move=MoveType.MOV_4, played=False
    )
    db.add(available_card4)
    db.commit()

    # Asigna las cartas de movimiento
    cards.assign_movement_cards(game_id=1, player_id=player.id, db=db)

    # Verifica que el jugador tenga 3 cartas
    cards_in_hand = (
        db.query(CardMove).filter(CardMove.owner_id == player.id).all()
    )
    assert (
        len(cards_in_hand) == 3
    ), "El jugador debería tener 3 cartas de movimiento en la mano."

    # --------------------------- ONE SLOT PLAYED -----------------------------------
    available_card1.played = True
    db.commit()
    cards_not_played = (
        db.query(CardMove)
        .filter(CardMove.owner_id == player.id, CardMove.played == False)
        .all()
    )

    assert len(cards_not_played) == 2, "El jugador ya jugo una de sus 3 cartas"

    # Asigna las cartas de movimiento
    cards.assign_movement_cards(game_id=1, player_id=player.id, db=db)

    # Verifica que el jugador tenga 3 cartas
    cards_not_played = (
        db.query(CardMove)
        .filter(CardMove.owner_id == player.id, CardMove.played == False)
        .all()
    )
    assert (
        len(cards_not_played) == 3
    ), "El jugador debería tener 3 cartas de movimiento en la mano."


def test_no_cards_unassign_when_no_movement_cards_exist():
    db = TestingSessionLocal()
    reset_db()

    player = create_player(db, 1)

    # No inicializa cartas de movimiento
    cards.unassign_played_movement_cards(player.id, db)

    # Verifica que el jugador siga sin cartas
    cards_in_hand = (
        db.query(CardMove).filter(CardMove.owner_id == player.id).all()
    )
    assert (
        len(cards_in_hand) == 0
    ), "El jugador no debería tener cartas de movimiento en la mano."


def test_no_cards_unassign_when_no_played_mov_cards():
    db = TestingSessionLocal()
    reset_db()

    player = create_player(db, 1)

    # Inicializa algunas cartas de movimiento disponibles con played=False
    card_moves = [
        CardMove(
            id=1,
            game_id=1,
            owner_id=player.id,
            move=MoveType.MOV_1,
            played=False,
        ),
        CardMove(
            id=2,
            game_id=1,
            owner_id=player.id,
            move=MoveType.MOV_2,
            played=False,
        ),
        CardMove(
            id=3,
            game_id=1,
            owner_id=player.id,
            move=MoveType.MOV_3,
            played=False,
        ),
    ]
    db.add_all(card_moves)
    db.commit()

    # Intenta eliminar las cartas de movimiento jugadas, pero no hay cartas de movimiento jugadas.
    cards.unassign_played_movement_cards(player.id, db)

    # Verifica que el jugador tenga 3 cartas
    cards_in_hand = (
        db.query(CardMove).filter(CardMove.owner_id == player.id).all()
    )

    assert (
        len(cards_in_hand) == 3
    ), "El jugador debería tener 3 cartas de movimiento en la mano."

    # Verifica que las cartas existen en la base de datos
    total_cards = db.query(CardMove).all()

    assert (
        len(total_cards) == 3
    ), "Deberían existir 3 cartas de movimiento en la base de datos."


def test_unassign_played_movement_cards():
    db = TestingSessionLocal()
    reset_db()

    player = create_player(db, 1)

    # Inicializa algunas cartas de movimiento disponibles con played=False
    card_moves = [
        CardMove(
            id=1,
            game_id=1,
            owner_id=player.id,
            move=MoveType.MOV_1,
            played=True,
        ),
        CardMove(
            id=2,
            game_id=1,
            owner_id=player.id,
            move=MoveType.MOV_2,
            played=False,
        ),
        CardMove(
            id=3,
            game_id=1,
            owner_id=player.id,
            move=MoveType.MOV_3,
            played=True,
        ),
    ]
    db.add_all(card_moves)
    db.commit()

    # Elimina las cartas de movimiento jugadas
    cards.unassign_played_movement_cards(player.id, db)

    # Verifica que el jugador tenga 1 carta
    cards_in_hand = (
        db.query(CardMove).filter(CardMove.owner_id == player.id).all()
    )
    assert (
        len(cards_in_hand) == 1
    ), "El jugador debería tener 1 carta de movimiento en la mano."
    assert (
        cards_in_hand[0].id == 2
    ), "La carta de movimiento no jugada debería ser la carta con ID 2."
    assert (
        cards_in_hand[0].played == False
    ), "La carta de movimiento no jugada no debería estar jugada."

    # Verifica que las cartas existen en la base de datos
    total_cards = db.query(CardMove).all()

    assert (
        len(total_cards) == 3
    ), "Deberían existir 3 cartas de movimiento en la base de datos."

    # Verifica que solo se han revocado las cartas jugadas.
    non_owned_cards = (
        db.query(CardMove).filter(CardMove.owner_id == None).all()
    )

    assert (
        len(non_owned_cards) == 2
    ), "No deberían existir cartas de movimiento sin dueño en la base de datos."

    for card in non_owned_cards:
        assert (
            card.played == False
        ), "Las cartas de movimiento sin dueño no deberían estar jugadas."
