from pydantic import BaseModel
from typing import (
    Deque, Dict, FrozenSet, List, Optional, Sequence, Set, Tuple, Union
)
from datetime import datetime
from beanie import Document


class Users(Document):
    Keywords = []
    email = ''
    created = ''
    city = ''

    def __int__(self, keywords, email, created, city):
        self.Keywords = keywords
        self.email = email
        self.created = created
        self.city = city

    def to_bson(self):
        data = self.dict(by_alias=True, exclude_none=True)
        if data["_id"] is None:
            data.pop("_id")
        return data


class Keywords(Document):
    # TODO- later define the structre of this "object" in reality its an article
    agriculture: List[object]
    business: List[object]
    elon: List[object]
    space: List[object]
    science: List[object]
    tech: List[object]
    war: List[object]
    motorsport: List[object]


class ArticleSDDescription(Document):
    source: Dict[str, str] = None
    description: str = None
