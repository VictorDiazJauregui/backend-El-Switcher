from app.models.playerlock import PlayerAction, PlayerLock, lock_player
from app.errors.handlers import ForbiddenError
import pytest


@pytest.fixture(autouse=True)
def reset_player_lock():
    """Fixture que resetea el estado de PlayerLock antes de cada prueba."""
    PlayerLock._instance = (
        None  # Resetea la instancia singleton para asegurar un estado limpio
    )


@pytest.fixture
def player_lock():
    return PlayerLock()


@pytest.fixture
def player_data():
    return {"player_id": 1, "action": PlayerAction.END_TURN}


def test_acquire_and_release_lock(player_lock, player_data):
    player_id = player_data["player_id"]
    action = player_data["action"]

    # Asegura que no hay bloqueo antes de adquirirlo
    assert not player_lock.is_locked(
        player_id, action
    ), "Player should not be locked"

    # Adquiere el bloqueo
    player_lock.acquire(player_id, action)
    assert player_lock.is_locked(player_id, action), "Player should be locked"

    # Libera el bloqueo
    player_lock.release(player_id, action)
    assert not player_lock.is_locked(
        player_id, action
    ), "Player should not be locked"


def test_acquire_lock_twice_raises_error(player_lock, player_data):
    player_id = player_data["player_id"]
    action = player_data["action"]

    # Adquiere el bloqueo
    player_lock.acquire(player_id, action)

    # Intentar adquirir el mismo bloqueo debe lanzar un ForbiddenError
    with pytest.raises(
        ForbiddenError, match="Player is currently in a game action"
    ):
        player_lock.acquire(player_id, action)


def test_release_non_existent_lock_does_nothing(player_lock, player_data):
    player_id = player_data["player_id"]
    action = player_data["action"]

    # Asegura que no hay bloqueo para este jugador/acción
    assert not player_lock.is_locked(
        player_id, action
    ), "Player should not be locked"

    # Liberar un bloqueo inexistente no debe causar errores
    player_lock.release(player_id, action)

    # Asegura que sigue sin haber bloqueo
    assert not player_lock.is_locked(
        player_id, action
    ), "Player should not be locked"


def test_lock_player_context_manager(player_data):
    player_id = player_data["player_id"]
    action = player_data["action"]

    # Asegura que el jugador no está bloqueado antes del uso del context manager
    player_lock = PlayerLock()
    assert not player_lock.is_locked(
        player_id, action
    ), "Player should not be locked"

    # Usa el context manager para adquirir y liberar el bloqueo automáticamente
    with lock_player(player_id, action):
        assert player_lock.is_locked(
            player_id, action
        ), "Player should be locked"

    # Asegura que el jugador ha sido liberado después del uso del context manager
    assert not player_lock.is_locked(
        player_id, action
    ), "Player should not be locked"


def test_lock_player_context_manager_raises_error_if_locked(
    player_lock, player_data
):
    player_id = player_data["player_id"]
    action = player_data["action"]

    # Bloquea al jugador antes de usar el context manager
    player_lock.acquire(player_id, action)

    # Intentar adquirir el mismo bloqueo dentro del context manager debe lanzar ForbiddenError
    with pytest.raises(
        ForbiddenError, match="Player is currently in a game action"
    ):
        with lock_player(player_id, action):
            pass  # No debería llegar aquí
