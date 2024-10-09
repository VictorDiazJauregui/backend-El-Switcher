from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func, select, case, exists
from typing import List, Dict


from app.schemas.cards import CardFigSchema, CardFigResponseSchema, CardMoveResponseSchema
from app.db.db import Player, CardMove, CardFig, MoveType, FigureType, Game
separador = "---------------------------------------------------------------------------------------------------"

def add_cards_to_db(game_id: int, db: Session) -> int:
    # If game exists
    game = db.query(Game).filter_by(id=game_id).first() is not None
    if game:
        moves = []
        figs = []
        
        move_count = db.query(func.count(CardMove.id)).filter(CardMove.game_id == game_id).scalar()
        fig_count = db.query(func.count(CardFig.id)).filter(CardFig.game_id == game_id).scalar()

        if move_count == 0:
            for move_type in MoveType:
                for _ in range(7):  # Create 7 cards of each type
                    moves.append(CardMove(game_id=game_id, move=move_type))

        if fig_count == 0:
            for figure_type in FigureType:
                for _ in range(2):  # Create 2 cards of each type
                    figs.append(CardFig(game_id=game_id, figure=figure_type))

        # Add all cards to database
        db.add_all(moves)
        db.add_all(figs)  
        db.commit()

        return 1 # success i guess...
    else:
        raise HTTPException("Game does not exist.")


def search_for_cards_to_deal(MovOrFig, game_id, number_of_cards_to_deal, db):
    available_cards = db.query(MovOrFig).filter(MovOrFig.owner_id == None, MovOrFig.game_id == game_id) \
                     .order_by(func.random()).limit(number_of_cards_to_deal).all()

    return available_cards

def deal_movement_cards(game_id: int, player_id: int, db: Session):
    player = db.execute(select(Player).where(Player.id == player_id)).scalars().first()
    # Get the current cards of the player
    dealt_cards = []
    cards_in_hand = db.query(CardMove).filter(CardMove.owner_id == player.id).all()
    for card in cards_in_hand:
        dealt_cards.append(CardMoveResponseSchema(
            movementcardId=card.id,
            type=card.move.value[1]
        ).model_dump())

    # Add more cards if the player has less than 3 cards
    if len(cards_in_hand) < 3:
        number_of_cards_to_deal = 3 - len(cards_in_hand)
        random_cards = search_for_cards_to_deal(CardMove, game_id, number_of_cards_to_deal, db)

        for card in random_cards:
            card.owner_id = player.id
            movecard = CardMoveResponseSchema(
                movementcardId=card.id,
                type=card.move.value[1]
            ).model_dump()
            dealt_cards.append(movecard)



    db.commit()
    return dealt_cards

def assign_figure_cards(game_id: int, player_id: int, db: Session):
    player = db.execute(select(Player).where(Player.id == player_id)).scalars().first()

    # Get the current cards of the player
    cards_in_hand = db.query(CardFig).filter(CardFig.owner_id == player.id).all()

    hasBlock = db.execute(select(exists().where(CardFig.owner_id == player_id).where(CardFig.block == True))).scalar()

    # Add more cards if the player has less than 3 cards and doesn't have a blocked card
    if len(cards_in_hand) < 3 and not hasBlock:
        number_of_cards_to_deal = 3 - len(cards_in_hand)
        random_cards = search_for_cards_to_deal(CardFig, game_id, number_of_cards_to_deal, db)

        for card in random_cards:
            card.owner_id = player.id


    db.commit()
    return 1


def deal_figure_cards(game_id: int, db: Session):
    list_of_ids = db.execute(select(Player.id).where(Player.game_id == game_id)).scalars().all()

    response = []
    dealt_cards = []
    for player_id in list_of_ids:
        cards_in_hand = db.query(CardFig).filter(CardFig.owner_id == player_id).all()
        for card in cards_in_hand:
            dealt_cards.append(CardFigSchema(
                    figureCardId=card.id,
                    difficulty="easy" if "EASY" in card.figure.name else "hard",
                    figureType=card.figure.value[0]
                ).model_dump())
        player_cards = {
            "ownerId": player_id,
            "cards": dealt_cards
        }
        dealt_cards = []
        response.append(player_cards)
    

    return response

def initialize_cards(game_id: int, db: Session):
    list_of_ids = db.execute(select(Player.id).where(Player.game_id == game_id)).scalars().all()
    print(f"LISTA DE IDS: {list_of_ids}")
    for player_id in list_of_ids:
        assign_figure_cards(game_id, player_id, db)
