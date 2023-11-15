"""Database models for the codereview app.

"""

from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel

class CustomModel(BaseModel):

    def __getitem__(self, item):
        return getattr(self, item)

    def __setitem__(self, item, value):
        setattr(self, item, value)

class Module(CustomModel):
    id: Optional[int]
    path: str
    first_reviewed: Optional[datetime]
    last_reviewed: Optional[datetime]
    first_snapshot: Optional[int]
    last_snapshot: Optional[int]

class Run(CustomModel):
    id: Optional[int]
    timestamp: datetime
    files_analyzed: List[str]

class Snapshot(CustomModel):
    id: Optional[int]
    snapshot_id: str
    timestamp: datetime
    summary: str
    module_id: int

class Message(CustomModel):
    id: Optional[int]
    timestamp: datetime
    content: str

class Review(CustomModel):
    id: Optional[int]
    timestamp: datetime
    content: str
