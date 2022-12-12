from pydantic import BaseModel
from typing import (
    Deque, Dict, FrozenSet, List, Optional, Sequence, Set, Tuple, Union
)
from datetime import datetime
from beanie import Document

class Users(Document):
    Keywords: list
    email: str
    created: str #'2032-04-23T10:20:30.400+02:30'
    city: str

    def to_bson(self):
        data = self.dict(by_alias=True, exclude_none=True)
        if data["_id"] is None:
            data.pop("_id")
        return data

class Keywords(Document):
    #TODO- later define the structre of this "object" in reality its an article
    agriculture: List[object]
    business: List[object]
    elon: List[object]
    space: List[object]
    science: List[object]
    tech: List[object]
    war: List[object]
    motosport: List[object]

class ArticleSDDescription(Document):
    source: Dict[str, str] = None
    description: str = None

