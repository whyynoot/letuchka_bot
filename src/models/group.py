import uuid
from dataclasses import dataclass


@dataclass
class RawGroup:
    name: str
    open: bool

@dataclass
class Group(RawGroup):
    id: uuid.UUID
