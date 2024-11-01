import asyncio
from app.models.broadcast import Broadcast
from app.routers import sio_game as sio
from app.services import game

TURN_TIME_LIMIT = 120

timer_tasks = {}    # Global dictionary to keep track of timer tasks


def stop_timer(game_id):

    if game_id in timer_tasks:
        timer_tasks[game_id].cancel()
        del timer_tasks[game_id]


def start_timer(game_id, player_id, db):

    timer_tasks[game_id] = asyncio.create_task(
        emit_timer(game_id, player_id, db)
    )

async def handle_timer(game_id, player_id, db):

    stop_timer(game_id)
    start_timer(game_id, player_id, db)

async def emit_timer(game_id, player_id, db):

    broadcast = Broadcast()
    time_left = TURN_TIME_LIMIT

    while time_left > 0:
        await broadcast.broadcast(
            sio.sio_game, game_id, "timer", {"time": time_left}
        )
        await asyncio.sleep(1)
        time_left -= 1

    await game.end_turn(game_id, player_id, db)
