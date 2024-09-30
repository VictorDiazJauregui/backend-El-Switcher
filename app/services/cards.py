from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func, select, case
from typing import List, Dict


from app.schemas.cards import CardFigSchema, CardFigResponseSchema, CardMoveResponseSchema
from app.db.db import Player, CardMove, CardFig, MoveType, FigureType


def add_cards_to_db(game_id: int, db: Session) -> int:
    moves = []
    figs = []

    for move_type in MoveType:
        for _ in range(7):  # Create 7 cards of each type
            moves.append(CardMove(game_id=game_id, move=move_type))

    for figure_type in FigureType:
        for _ in range(2):  # Create 2 cards of each type
            figs.append(CardFig(game_id=game_id, figure=figure_type))

    # Add all cards to database
    db.add_all(moves)
    db.add_all(figs)  
    db.commit()

    return 1 # success i guess...


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

    # Add more cards if the player has less than 3 cards and doesn't have a blocked card
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

def deal_figure_cards(game_id: int, db: Session):
    players_info = db.execute(select(
        Player.id,
        func.count(CardFig.id).label('card_figs_count'),
        func.max(case((CardFig.block == True, 1), else_=0)).label('has_blocked_card')
    ).outerjoin(CardFig, CardFig.owner_id == Player.id)
    .where(Player.game_id == game_id)
    .group_by(Player.id, Player.name)).mappings().all()

    all_responses = []  # responses fro al;l players

    for player in players_info:
        dealt_cards = []

        # Get the current cards of the player
        cards_in_hand = db.query(CardFig).filter(CardFig.owner_id == player["id"]).all()
        for card in cards_in_hand:
            dealt_cards.append(CardFigSchema(
                figureCardId=card.id,
                difficulty="easy" if "EASY" in card.figure.name else "hard"
            ))

        # Add more cards if the player has less than 3 cards and doesn't have a blocked card
        if player['card_figs_count'] < 3 and not player['has_blocked_card']:
            number_of_cards_to_deal = 3 - player['card_figs_count']
            random_cards = search_for_cards_to_deal(CardFig, game_id, number_of_cards_to_deal, db)

            for card in random_cards:
                card.owner_id = player['id']
                figurecard = CardFigSchema(
                    figureCardId=card.id,
                    difficulty="easy" if "EASY" in card.figure.name else "hard"
                )
                dealt_cards.append(figurecard)

        
        response = CardFigResponseSchema(ownerId=player["id"], cards=dealt_cards)
        all_responses.append(response)

    db.commit()
    return [response.model_dump() for response in all_responses]
            

