import asyncio
from app.db.db import (
    Game,
    Board,
    ParallelBoard,
    CardMove,
    CardFig,
    SquarePiece,
    SessionLocal,
    LogMessage,
    ChatMessage,
)

"""
Cleanup game data from the database.

This asynchronous function performs a series of cleanup operations for a given game.

It sets the game status to FINISHED, waits for 10 seconds, and then deletes all related
data from various tables in the database, including players, boards, parallel boards,
card moves, card figures, and square pieces. Finally, it deletes the game itself and
commits the changes to the database.

"""


async def cleanup_game(game_id):

    await asyncio.sleep(5)
    with SessionLocal() as db:
        game = db.query(Game).filter(Game.id == game_id).first()
        game_name = game.name

        # Delete all card figures related to the game
        db.query(CardFig).filter(CardFig.game_id == game_id).delete()

        # Delete all card moves related to the game
        db.query(CardMove).filter(CardMove.game_id == game_id).delete()

        if game.players:
            for player in game.players:
                db.delete(player)
                db.commit()

        # Delete all square pieces related to the game
        db.query(SquarePiece).filter(SquarePiece.board_id == game_id).delete()

        # Delete all parallel boards related to the game
        db.query(ParallelBoard).filter(
            ParallelBoard.board_id == game_id
        ).delete()

        # Delete all boards related to the game
        db.query(Board).filter(Board.game_id == game_id).delete()

        # Delete all chat messages related to the game
        db.query(ChatMessage).filter(ChatMessage.game_id == game_id).delete()

        # Delete all log messages related to the game
        db.query(LogMessage).filter(LogMessage.game_id == game_id).delete()

        # Delete the game itself
        db.query(Game).filter(Game.id == game_id).delete()

        # Commit the changes to the database
        db.commit()
        print(f"Game {game_name} ID:{game_id} data has been cleaned up.")

        return {"message": f"Game {game_id} has been cleaned up."}
