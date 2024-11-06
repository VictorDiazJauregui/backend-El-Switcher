from pydantic import BaseModel
from typing import List, Literal


class ChatSendMessageSchema(BaseModel):
    """
    What the client sends to us
    """

    playerId: int
    message: str


class ChatMessageSchema(BaseModel):
    """
    What we're going to send the client
    """

    writtenBy: str
    message: str


class SingleChatMessageSchema(BaseModel):
    type: Literal["singleMessage"] = "singleMessage"
    data: ChatMessageSchema


class MultipleChatMessagesSchema(BaseModel):
    type: Literal["multipleMessages"] = "multipleMessages"
    data: List[ChatMessageSchema]
