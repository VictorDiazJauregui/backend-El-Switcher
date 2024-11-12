from random import shuffle

from sqlalchemy.orm import Session
from sqlalchemy import func, select, exists
from sqlalchemy.exc import SQLAlchemyError

from app.db.db import (
    CardMove,
    CardFig,
    FigureType,
    Game,
    MoveType,
    Player,
)
from app.errors.handlers import NotFoundError
from app.schemas.cards import (
    CardFigSchema,
    CardFigResponseSchema,
    CardMoveResponseSchema,
)


def add_cards_to_db(game_id: int, db: Session) -> int:
    """
    Adds all cards to be used in the game to the database.
    """

    # If game exists
    try:
        game = db.query(Game).filter_by(id=game_id).first() is not None
        if game:
            moves = []
            figs = []

            move_count = (
                db.query(func.count(CardMove.id))
                .filter(CardMove.game_id == game_id)
                .scalar()
            )
            fig_count = (
                db.query(func.count(CardFig.id))
                .filter(CardFig.game_id == game_id)
                .scalar()
            )

            if move_count == 0:
                for move_type in MoveType:
                    for _ in range(7):  # Create 7 cards of each type
                        moves.append(CardMove(game_id=game_id, move=move_type))

            if fig_count == 0:
                for figure_type in FigureType:
                    for _ in range(2):  # Create 2 cards of each type
                        figs.append(
                            CardFig(game_id=game_id, figure=figure_type)
                        )

            # Add all cards to database
            db.add_all(moves)
            db.add_all(figs)
            db.commit()

            return 1  # success i guess...
        else:
            raise NotFoundError("Game does not exist.")
    except SQLAlchemyError as e:
        raise Exception(f"Error adding cards: {e}")


def distribute_cards_to_deck(game_id: int, db: Session):
    """
    Make it fair by assigning the same amount of hard/easy cards
    to each player.
    """
    try:
        list_of_ids = (
            db.execute(select(Player.id).where(Player.game_id == game_id))
            .scalars()
            .all()
        )
        number_of_players = len(list_of_ids)
        num_of_easy_per_deck = 14 // number_of_players
        num_of_hard_per_deck = 36 // number_of_players

        figure_cards = (
            db.query(CardFig).filter(CardFig.game_id == game_id).all()
        )
        easy_cards = [
            card for card in figure_cards if "EASY" in card.figure.name
        ]
        hard_cards = [
            card for card in figure_cards if "HARD" in card.figure.name
        ]
        shuffle(easy_cards)
        shuffle(hard_cards)

        for player_id in list_of_ids:
            player_easy_cards = easy_cards[
                :num_of_easy_per_deck
            ]  # This selects only the needed number of cards
            player_hard_cards = hard_cards[:num_of_hard_per_deck]

            for card in player_easy_cards:
                card.owner_id = player_id
            for card in player_hard_cards:
                card.owner_id = player_id

            easy_cards = easy_cards[
                num_of_easy_per_deck:
            ]  # We don't need the assigned cards anymore
            hard_cards = hard_cards[num_of_hard_per_deck:]

        db.commit()

    except SQLAlchemyError as e:
        raise Exception(f"Error creating decks: {e}")


def search_for_fig_cards_to_deal(
    CardFig,
    game_id: int,
    number_of_cards_to_deal: int,
    player_id: int,
    db: Session,
):
    """
    Searches the db for cards belonging to the player's deck.
    """
    try:
        available_cards = (
            db.query(CardFig)
            .filter(
                CardFig.owner_id == player_id,
                CardFig.game_id == game_id,
                CardFig.in_hand == False,
            )
            .order_by(func.random())
            .limit(number_of_cards_to_deal)
            .all()
        )

        return available_cards

    except SQLAlchemyError as e:
        raise Exception(f"Error searchig cards: {e}")


def search_for_mov_cards_to_deal(
    CardMove, game_id: int, number_of_cards_to_deal: int, db: Session
):
    """
    Searches the db for cards belonging to this game without an owner.
    """
    try:
        available_cards = (
            db.query(CardMove)
            .filter(CardMove.owner_id == None, CardMove.game_id == game_id)
            .order_by(func.random())
            .limit(number_of_cards_to_deal)
            .all()
        )

        return available_cards

    except SQLAlchemyError as e:
        raise Exception(f"Error searchig cards: {e}")


def assign_movement_cards(game_id: int, player_id: int, db: Session):
    """
    Assigns ownership of a card(s) to a player.
    """
    # try:
    player = (
        db.execute(select(Player).where(Player.id == player_id))
        .scalars()
        .first()
    )

    # Get the current cards that the player hasn't played
    cards_in_hand = (
        db.query(CardMove).filter(CardMove.owner_id == player.id).all()
    )
    remaining_cards = []
    for card in cards_in_hand:
        if card.played:
            card.owner_id = None
            card.played = False
        else:
            remaining_cards.append(card)

    cards_in_hand = remaining_cards

    # Add more cards if the player has less than 3 cards and doesn't have a blocked card
    if len(cards_in_hand) < 3:
        number_of_cards_to_deal = 3 - len(cards_in_hand)
        random_cards = search_for_mov_cards_to_deal(
            CardMove, game_id, number_of_cards_to_deal, db
        )

        for card in random_cards:
            card.owner_id = player.id

    db.commit()

    # except SQLAlchemyError as e:
    #    raise Exception(f"Error assigning movement cards: {e}")


def fetch_movement_cards(player_id: int, db: Session):
    """
    Fetches via queries the figure cards of every player and returns a format ready to be emitted.
    """
    try:
        dealt_cards = []
        cards_in_hand = (
            db.query(CardMove).filter(CardMove.owner_id == player_id).all()
        )
        for card in cards_in_hand:
            dealt_cards.append(
                CardMoveResponseSchema(
                    movementcardId=card.id,
                    type=card.move.value[1],
                    moveType=card.move.value[0],
                    played=card.played,
                ).model_dump()
            )

        return dealt_cards

    except SQLAlchemyError as e:
        raise Exception(f"Error fetching cards: {e}")


def assign_figure_cards(game_id: int, player_id: int, db: Session):
    """
    Assigns ownership of a card(s) to a player.
    """
    try:
        player = (
            db.execute(select(Player).where(Player.id == player_id))
            .scalars()
            .first()
        )

        # Get the current cards from the hand of the player
        cards_in_hand = (
            db.query(CardFig)
            .filter(CardFig.owner_id == player.id, CardFig.in_hand == True)
            .all()
        )

        hasBlock = db.execute(
            select(
                exists()
                .where(CardFig.owner_id == player_id, CardFig.in_hand == True)
                .where(CardFig.block == True)
            )
        ).scalar()

        # Add more cards if the player has less than 3 cards and doesn't have a blocked card
        if len(cards_in_hand) < 3 and not hasBlock:
            number_of_cards_to_deal = 3 - len(cards_in_hand)
            if number_of_cards_to_deal < 0:
                raise Exception("INVALID NUMBER OF CARDS TO DEAL")
            random_cards = search_for_fig_cards_to_deal(
                CardFig, game_id, number_of_cards_to_deal, player_id, db
            )

            for card in random_cards:
                card.in_hand = True

        db.commit()

    except SQLAlchemyError as e:
        raise Exception(f"Error assigning figure cards: {e}")


def fetch_figure_cards(game_id: int, db: Session):
    """
    Fetches via queries the figure cards of every player and returns a format ready to be emitted.
    """
    try:
        list_of_ids = (
            db.execute(select(Player.id).where(Player.game_id == game_id))
            .scalars()
            .all()
        )

        response = []
        dealt_cards = []
        for player_id in list_of_ids:
            cards_in_hand = (
                db.query(CardFig)
                .filter(CardFig.owner_id == player_id, CardFig.in_hand == True)
                .all()
            )
            for card in cards_in_hand:
                dealt_cards.append(
                    CardFigSchema(
                        figureCardId=card.id,
                        difficulty=(
                            "easy" if "EASY" in card.figure.name else "hard"
                        ),
                        figureType=card.figure.value[0],
                        isBlocked=card.block,
                    ).model_dump()
                )
            player_cards = CardFigResponseSchema(
                ownerId=player_id, cards=dealt_cards
            ).model_dump()
            dealt_cards = []
            response.append(player_cards)

        return response

    except SQLAlchemyError as e:
        raise Exception(f"Error fetching cards: {e}")


def delete_figure_card(figureCardId: int, db: Session):
    """
    Deletes a figure card from the database.
    """
    try:
        card_sacrifice = (
            db.execute(select(CardFig).where(CardFig.id == figureCardId))
            .scalars()
            .first()
        )
        if not card_sacrifice:
            raise Exception(f"Error deleting figure card: {e}")
        db.delete(card_sacrifice)
        db.commit()

    except SQLAlchemyError as e:
        raise Exception(f"Error deleting figure card: {e}")


def unassign_played_movement_cards(player_id: int, db: Session):
    """
    Unassigns the played movement cards for the specified player by marking them
    as unplayed and removing their ownership.
    """
    try:
        cards_in_hand = (
            db.query(CardMove).filter(CardMove.owner_id == player_id).all()
        )
        for card in cards_in_hand:
            if card.played:
                card.played = False
                card.owner_id = None
        db.commit()
    except SQLAlchemyError as e:
        raise Exception(f"Error deleting played movement cards: {e}")


def initialize_cards(game_id: int, db: Session):
    """
    Called at the start of the game. Assigns 3 cards to each player's hand
    and creates each player's figure deck.
    """
    try:
        distribute_cards_to_deck(game_id, db)

        list_of_ids = (
            db.execute(select(Player.id).where(Player.game_id == game_id))
            .scalars()
            .all()
        )

        for player_id in list_of_ids:
            assign_figure_cards(game_id, player_id, db)
            assign_movement_cards(game_id, player_id, db)
    except SQLAlchemyError as e:
        raise Exception(f"Error initializing cards: {e}")


def unblock_card(player_id: int, db: Session):
    """
    Unblocks the player's blocked figure card if it's the
    only one left in their hand.
    """
    cards_in_hand = (
        db.query(CardFig)
        .filter(CardFig.owner_id == player_id, CardFig.in_hand == True)
        .all()
    )
    if cards_in_hand:
        the_only_card = cards_in_hand[0]
        if len(cards_in_hand) == 1 and the_only_card.block == True:
            the_only_card.block = False

        db.commit()
    else:
        return
