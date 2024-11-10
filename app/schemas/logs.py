from pydantic import BaseModel
from typing import List, Literal


class LogMessageSchema(BaseModel):
    message: str


class SingleLogMessageSchema(BaseModel):
    type: Literal["singleLog"] = "singleLog"
    data: LogMessageSchema


class MultipleLogMessagesSchema(BaseModel):
    type: Literal["multipleLogs"] = "multipleLogs"
    data: List[LogMessageSchema]
