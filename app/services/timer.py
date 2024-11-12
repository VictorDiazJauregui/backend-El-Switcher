import asyncio
from app.models.broadcast import Broadcast
from app.routers import sio_game as sio
from app.services import game
from app.services.game_player_service import get_game, get_player
from app.services import game_events

TURN_TIME_LIMIT = 120

timer_tasks = {}  # Global dictionary to keep track of timer tasks
time_left_tasks = {}  # Global dictionary to keep track of time left for tasks


def stop_timer(game_id):

    if game_id in timer_tasks:
        timer_tasks[game_id].cancel()
        del timer_tasks[game_id]

    if game_id in time_left_tasks:
        del time_left_tasks[game_id]


def start_timer(game_id, player_id, db):

    if game_id not in time_left_tasks:
        time_left_tasks[game_id] = TURN_TIME_LIMIT

    timer_tasks[game_id] = asyncio.create_task(
        emit_timer(game_id, player_id, db)
    )


async def restart_timer(game_id, player_id, db):

    stop_timer(game_id)
    start_timer(game_id, player_id, db)


async def emit_timer(game_id, player_id, db):

    broadcast = Broadcast()
    time_left = time_left_tasks[game_id]

    player = get_player(player_id, db)
    game_ = get_game(game_id, db)

    while time_left > 0:
        time_left_tasks[game_id] = time_left
        await broadcast.broadcast(
            sio.sio_game, game_id, "timer", {"time": time_left}
        )
        await asyncio.sleep(1)
        time_left -= 1

    if player.turn == game_.turn:
        await game_events.emit_log(
            game_id, f"Ups! El tiempo para {player.name} ha terminado...", db
        )
        await game.end_turn(game_id, player_id, db)


async def get_current_timer(game_id):
    if game_id in time_left_tasks:
        return time_left_tasks[game_id]
    return None


async def get_current_task(game_id):
    if game_id in timer_tasks:
        return timer_tasks[game_id]
    return None


def cancel_timer(game_id):
    if game_id in timer_tasks:
        timer_tasks[game_id].cancel()
        del timer_tasks[game_id]
