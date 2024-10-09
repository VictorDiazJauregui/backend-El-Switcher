from app.db.db import Player, Game
from app.schemas.player import PlayerResponseSchema, WinnerSchema
from app.models.broadcast import Broadcast
from app.services.cards import fetch_figure_cards, fetch_movement_cards
from app.services.board import get_board
from app.routers import sio_game as sio

async def disconnect_player_socket(player_id, game_id):
    broadcast = Broadcast()
    await broadcast.unregister_player_socket(sio.sio_game, player_id, game_id)

async def emit_players_game(game_id, db):
    players = db.query(Player).filter(Player.game_id == game_id).all()

    #convert every player in player response schema
    PlayerResponseSchemaList = []

    for player in players:
        PlayerResponseSchemaList.append(PlayerResponseSchema(playerId=player.id, playerName=player.name).model_dump())

    broadcast = Broadcast()

    # send the player list to all players in the lobby
    await broadcast.broadcast(sio.sio_game, game_id, 'player_list', PlayerResponseSchemaList)

async def emit_turn_info(game_id, db):
    game = db.query(Game).filter(Game.id == game_id).first()

    player = db.query(Player).filter(Player.game_id == game_id, Player.turn == game.turn).first()

    broadcast = Broadcast()

    turn_info = {
        "playerTurnId": player.id,
    }

    # send the turn info to all players in the lobby
    await broadcast.broadcast(sio.sio_game, game_id, 'turn', turn_info)

async def emit_winner(game_id, winner_id, db):
    winner = db.query(Player).filter(Player.id == winner_id).first()

    broadcast = Broadcast()


    await broadcast.broadcast(sio.sio_game, game_id, 'winner', WinnerSchema(idWinner=winner.id, nameWinner=winner.name).model_dump())

async def emit_cards(game_id, player_id, db):
    """
    Emits to specified player their own movement cards and all other player's figure cards.
    """
    channel = Broadcast()

    total_figure_cards = fetch_figure_cards(game_id, db)
    player_move_cards = fetch_movement_cards(game_id, db)

    await channel.broadcast(sio=sio.sio_game, game_id=game_id, event='figure_cards', data=total_figure_cards)
    await channel.send_to_player(sio=sio.sio_game, player_id=player_id, event='movement_cards', data=player_move_cards)

async def emit_board(game_id, db):
    """
    Emits the current board.
    """
    channel = Broadcast()
    board = get_board(game_id, db)
    
    await channel.broadcast(sio.sio_game, game_id, 'board', board)
