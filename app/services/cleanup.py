import asyncio

from app.db.db import (
    Game,
    GameStatus,
    Player,
    Board,
    ParallelBoard,
    CardMove,
    CardFig,
    SquarePiece,
)


"""
Cleanup game data from the database.

This asynchronous function performs a series of cleanup operations for a given game.

It sets the game status to FINISHED, waits for 10 seconds, and then deletes all related
data from various tables in the database, including players, boards, parallel boards,
card moves, card figures, and square pieces. Finally, it deletes the game itself and
commits the changes to the database.

"""


async def cleanup_game(game_id, db):

    # Set the game status to FINISHED

    game = db.query(Game).filter(Game.id == game_id).first()
    game.status = GameStatus.FINISHED
    db.commit()

    # Sleep for 10 seconds
    await asyncio.sleep(10)

    # Delete all players related to the game
    db.query(Player).filter(Player.game_id == game_id).delete()

    # Delete all boards related to the game
    db.query(Board).filter(Board.game_id == game_id).delete()

    # Delete all parallel boards related to the game
    db.query(ParallelBoard).filter(ParallelBoard.board_id == game_id).delete()

    # Delete all card moves related to the game
    db.query(CardMove).filter(CardMove.game_id == game_id).delete()

    # Delete all card figures related to the game
    db.query(CardFig).filter(CardFig.game_id == game_id).delete()

    # Delete all square pieces related to the game
    db.query(SquarePiece).filter(SquarePiece.board_id == game_id).delete()

    # Delete the game itself
    db.query(Game).filter(Game.id == game_id).delete()

    # Commit the changes to the database
    db.commit()
