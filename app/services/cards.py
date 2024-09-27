from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func, select, case

from app.schemas.game import GameCreateSchema, GameListSchema, ListSchema, StartResponseSchema
from app.schemas.player import PlayerResponseSchema
from app.db.db import Game, Player, GameStatus, Turn, CardMove, CardFig, MoveType, FigureType



def add_cards_to_db(db: Session) -> int: # No se realmente que devolver
    moves = [
        CardMove(id=MoveType.MOV_1.value[0], move=MoveType.MOV_1),
        CardMove(id=MoveType.MOV_2.value[0], move=MoveType.MOV_2),
        CardMove(id=MoveType.MOV_3.value[0], move=MoveType.MOV_3),
        CardMove(id=MoveType.MOV_4.value[0], move=MoveType.MOV_4),
        CardMove(id=MoveType.MOV_5.value[0], move=MoveType.MOV_5),
        CardMove(id=MoveType.MOV_6.value[0], move=MoveType.MOV_6),
        CardMove(id=MoveType.MOV_7.value[0], move=MoveType.MOV_7),
        CardMove(id=MoveType.MOV_8.value[0], move=MoveType.MOV_8),
        CardMove(id=MoveType.MOV_9.value[0], move=MoveType.MOV_9),
        CardMove(id=MoveType.MOV_10.value[0], move=MoveType.MOV_10),
        CardMove(id=MoveType.MOV_11.value[0], move=MoveType.MOV_11),
        CardMove(id=MoveType.MOV_12.value[0], move=MoveType.MOV_12),
        CardMove(id=MoveType.MOV_13.value[0], move=MoveType.MOV_13),
        CardMove(id=MoveType.MOV_14.value[0], move=MoveType.MOV_14),
        CardMove(id=MoveType.MOV_15.value[0], move=MoveType.MOV_15),
        CardMove(id=MoveType.MOV_16.value[0], move=MoveType.MOV_16),
        CardMove(id=MoveType.MOV_17.value[0], move=MoveType.MOV_17),
        CardMove(id=MoveType.MOV_18.value[0], move=MoveType.MOV_18),
        CardMove(id=MoveType.MOV_19.value[0], move=MoveType.MOV_19),
        CardMove(id=MoveType.MOV_20.value[0], move=MoveType.MOV_20),
        CardMove(id=MoveType.MOV_21.value[0], move=MoveType.MOV_21),
        CardMove(id=MoveType.MOV_22.value[0], move=MoveType.MOV_22),
        CardMove(id=MoveType.MOV_23.value[0], move=MoveType.MOV_23),
        CardMove(id=MoveType.MOV_24.value[0], move=MoveType.MOV_24),
        CardMove(id=MoveType.MOV_25.value[0], move=MoveType.MOV_25),
        CardMove(id=MoveType.MOV_26.value[0], move=MoveType.MOV_26),
        CardMove(id=MoveType.MOV_27.value[0], move=MoveType.MOV_27),
        CardMove(id=MoveType.MOV_28.value[0], move=MoveType.MOV_28),
        CardMove(id=MoveType.MOV_29.value[0], move=MoveType.MOV_29),
        CardMove(id=MoveType.MOV_30.value[0], move=MoveType.MOV_30),
        CardMove(id=MoveType.MOV_31.value[0], move=MoveType.MOV_31),
        CardMove(id=MoveType.MOV_32.value[0], move=MoveType.MOV_32),
        CardMove(id=MoveType.MOV_33.value[0], move=MoveType.MOV_33),
        CardMove(id=MoveType.MOV_34.value[0], move=MoveType.MOV_34),
        CardMove(id=MoveType.MOV_35.value[0], move=MoveType.MOV_35),
        CardMove(id=MoveType.MOV_36.value[0], move=MoveType.MOV_36),
        CardMove(id=MoveType.MOV_37.value[0], move=MoveType.MOV_37),
        CardMove(id=MoveType.MOV_38.value[0], move=MoveType.MOV_38),
        CardMove(id=MoveType.MOV_39.value[0], move=MoveType.MOV_39),
        CardMove(id=MoveType.MOV_40.value[0], move=MoveType.MOV_40)
    ]

    figs = [
        CardFig(id=FigureType.EASY_1.value[0], figure=FigureType.EASY_1),
        CardFig(id=FigureType.EASY_2.value[0], figure=FigureType.EASY_2),
        CardFig(id=FigureType.EASY_3.value[0], figure=FigureType.EASY_3),
        CardFig(id=FigureType.EASY_4.value[0], figure=FigureType.EASY_4),
        CardFig(id=FigureType.EASY_5.value[0], figure=FigureType.EASY_5),
        CardFig(id=FigureType.EASY_6.value[0], figure=FigureType.EASY_6),
        CardFig(id=FigureType.EASY_7.value[0], figure=FigureType.EASY_7),
        
        CardFig(id=FigureType.HARD_1.value[0], figure=FigureType.HARD_1),
        CardFig(id=FigureType.HARD_2.value[0], figure=FigureType.HARD_2),
        CardFig(id=FigureType.HARD_3.value[0], figure=FigureType.HARD_3),
        CardFig(id=FigureType.HARD_4.value[0], figure=FigureType.HARD_4),
        CardFig(id=FigureType.HARD_5.value[0], figure=FigureType.HARD_5),
        CardFig(id=FigureType.HARD_6.value[0], figure=FigureType.HARD_6),
        CardFig(id=FigureType.HARD_7.value[0], figure=FigureType.HARD_7),
        CardFig(id=FigureType.HARD_8.value[0], figure=FigureType.HARD_8),
        CardFig(id=FigureType.HARD_9.value[0], figure=FigureType.HARD_9),
        CardFig(id=FigureType.HARD_10.value[0], figure=FigureType.HARD_10),
        CardFig(id=FigureType.HARD_11.value[0], figure=FigureType.HARD_11),
        CardFig(id=FigureType.HARD_12.value[0], figure=FigureType.HARD_12),
        CardFig(id=FigureType.HARD_13.value[0], figure=FigureType.HARD_13),
        CardFig(id=FigureType.HARD_14.value[0], figure=FigureType.HARD_14),
        CardFig(id=FigureType.HARD_15.value[0], figure=FigureType.HARD_15),
        CardFig(id=FigureType.HARD_16.value[0], figure=FigureType.HARD_16),
        CardFig(id=FigureType.HARD_17.value[0], figure=FigureType.HARD_17),
        CardFig(id=FigureType.HARD_18.value[0], figure=FigureType.HARD_18),

        # We need 2 of each card

        CardFig(id=FigureType.EASY_1.value[0], figure=FigureType.EASY_1),
        CardFig(id=FigureType.EASY_2.value[0], figure=FigureType.EASY_2),
        CardFig(id=FigureType.EASY_3.value[0], figure=FigureType.EASY_3),
        CardFig(id=FigureType.EASY_4.value[0], figure=FigureType.EASY_4),
        CardFig(id=FigureType.EASY_5.value[0], figure=FigureType.EASY_5),
        CardFig(id=FigureType.EASY_6.value[0], figure=FigureType.EASY_6),
        CardFig(id=FigureType.EASY_7.value[0], figure=FigureType.EASY_7),
        
        CardFig(id=FigureType.HARD_1.value[0], figure=FigureType.HARD_1),
        CardFig(id=FigureType.HARD_2.value[0], figure=FigureType.HARD_2),
        CardFig(id=FigureType.HARD_3.value[0], figure=FigureType.HARD_3),
        CardFig(id=FigureType.HARD_4.value[0], figure=FigureType.HARD_4),
        CardFig(id=FigureType.HARD_5.value[0], figure=FigureType.HARD_5),
        CardFig(id=FigureType.HARD_6.value[0], figure=FigureType.HARD_6),
        CardFig(id=FigureType.HARD_7.value[0], figure=FigureType.HARD_7),
        CardFig(id=FigureType.HARD_8.value[0], figure=FigureType.HARD_8),
        CardFig(id=FigureType.HARD_9.value[0], figure=FigureType.HARD_9),
        CardFig(id=FigureType.HARD_10.value[0], figure=FigureType.HARD_10),
        CardFig(id=FigureType.HARD_11.value[0], figure=FigureType.HARD_11),
        CardFig(id=FigureType.HARD_12.value[0], figure=FigureType.HARD_12),
        CardFig(id=FigureType.HARD_13.value[0], figure=FigureType.HARD_13),
        CardFig(id=FigureType.HARD_14.value[0], figure=FigureType.HARD_14),
        CardFig(id=FigureType.HARD_15.value[0], figure=FigureType.HARD_15),
        CardFig(id=FigureType.HARD_16.value[0], figure=FigureType.HARD_16),
        CardFig(id=FigureType.HARD_17.value[0], figure=FigureType.HARD_17),
        CardFig(id=FigureType.HARD_18.value[0], figure=FigureType.HARD_18)
    ]

    db.add(moves)
    db.add(figs)
    db.commit()

    return 1


def cards_deal(game_id: int, db: Session):
    # Probablemente deba usar el game_id en algun lado...

    players_info = db.execute(select(
        Player.id,
        Player.name,
        func.count(CardMove.id).label('card_moves_count'),
        func.count(CardFig.id).label('card_figs_count'),
        func.max(case([(CardFig.blocked == True, 1)], else_=0)).label('has_blocked_card')
    ).outerjoin(CardMove, CardMove.owner_id == Player.id)
    .outerjoin(CardFig, CardFig.owner_id == Player.id)
    .group_by(Player.id, Player.name)
    ).mappings().all()

    # List of players info where every player is a dictionary with its own info
    
    for player in players_info:
        if(player['card_moves_count'] != 3): # Movement Cards
            number_of_cards_to_deal = 3 - player['card_moves_count']
            random_cards = db.query(CardMove).filter(CardMove.owner_id == None) \
                            .order_by(func.random()).limit(number_of_cards_to_deal).all()
            
            for card in random_cards:
                 card.owner_id = player['id']
        

        if(player['card_figs_count'] != 3 and not player['has_blocked_card']): # Figure Cards
            number_of_cards_to_deal = 3 - player['card_figs_count']
            random_cards = db.query(CardFig).filter(CardFig.owner_id == None) \
                            .order_by(func.random()).limit(number_of_cards_to_deal).all()
            
            for card in random_cards:
                 card.owner_id = player['id']

    db.commit()