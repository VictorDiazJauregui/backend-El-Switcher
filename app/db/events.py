from sqlalchemy import event
from app.db.models.card_move import CardMove
from app.db.models.player import Player


# Event listener to set owner_id to None instead of deleting CardMove
@event.listens_for(Player, "before_delete")
def receive_before_delete(mapper, connection, target):
    # Set owner_id to None if it is not already None
    connection.execute(
        CardMove.__table__.update()
        .where(CardMove.owner_id == target.id)
        .values(owner_id=None)
    )
    # Delete CardMove if owner_id is already None
    connection.execute(
        CardMove.__table__.delete()
        .where(CardMove.owner_id == target.id)
        .where(CardMove.owner_id.is_(None))
    )
