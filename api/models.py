from pydantic import BaseModel
from typing import List


class Zone(BaseModel):
    id: str
    capacity: str
    price: str
    name: str
    numbered: str


class Event(BaseModel):
    title: str
    start_date: str
    end_date: str
    event_id: str
    sell_from: str
    sell_to: str
    sold_out: str
    zones: List[Zone]
