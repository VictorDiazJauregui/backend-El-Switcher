from app.errors.handlers import ForbiddenError
from enum import Enum
from contextlib import contextmanager


class PlayerAction(Enum):
    END_TURN = "end_turn"
    REMOVE_PLAYER = "remove_player"


class PlayerLock:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(PlayerLock, cls).__new__(cls)
            # Inicializa los bloqueos de los jugadores para cada acción
            cls._instance.locks = {action: {} for action in PlayerAction}
        return cls._instance

    def is_locked(self, player_id: int, action: PlayerAction) -> bool:
        """Verifica si un jugador está bloqueado para una acción específica."""
        return player_id in self.locks[action]

    def acquire(self, player_id: int, action: PlayerAction) -> None:
        """Bloquea un jugador para una acción específica."""
        if self.is_locked(player_id, action):
            raise ForbiddenError(
                f"Player is currently in a game action ({action.value}) and cannot perform another action."
            )
        self.locks[action][player_id] = action

    def release(self, player_id: int, action: PlayerAction) -> None:
        """Desbloquea un jugador para una acción específica."""
        if player_id in self.locks[action]:
            del self.locks[action][player_id]


@contextmanager
def lock_player(player_id: int, action: PlayerAction):
    """Context manager para bloquear un jugador para una acción específica."""
    player_lock = PlayerLock()
    player_lock.acquire(player_id, action)
    try:
        yield
    finally:
        player_lock.release(player_id, action)
