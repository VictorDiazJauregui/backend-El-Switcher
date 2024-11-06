from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schemas.chat import (
    ChatMessageSchema,
    ChatSendMessageSchema,
    SingleChatMessageSchema,
)
from app.db.db import get_db, ChatMessage
from app.services.game_player_service import get_player
from app.services.game_events import emit_single_chat_message

router = APIRouter()


@router.post("/game/{game_id}/send_message")
async def send_message(
    chatMessageInfo: ChatSendMessageSchema,
    game_id: int,
    db: Session = Depends(get_db),
):
    """
    Sends (broadcasts) the message written by the user in the game's chat
    to all other players in the room
    """
    player = get_player(chatMessageInfo.playerId, db)
    if not player or player.game_id != game_id:
        raise Exception("Player not found or not in game")

    message = ChatMessageSchema(
        writtenBy=player.name, message=chatMessageInfo.message
    )
    singleMessage = SingleChatMessageSchema(data=message).model_dump()

    db.add(
        ChatMessage(
            message=chatMessageInfo.message,
            sender_id=chatMessageInfo.playerId,
            game_id=player.game_id,
        )
    )
    db.commit()

    await emit_single_chat_message(
        message=singleMessage, game_id=player.game_id
    )

    return 204
