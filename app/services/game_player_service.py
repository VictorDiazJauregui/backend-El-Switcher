from sqlalchemy.orm import Session
from app.db.db import Game, Player
from app.errors.handlers import NotFoundError


def get_game(game_id: int, db: Session) -> Game:
    game = db.query(Game).filter(Game.id == game_id).first()
    if game is None:
        raise NotFoundError(f"Game with id {game_id} does not exist.")
    return game


def get_player(player_id: int, db: Session) -> Player:
    player = db.query(Player).filter(Player.id == player_id).first()
    if player is None:
        raise NotFoundError(f"Player with id {player_id} does not exist.")
    return player
