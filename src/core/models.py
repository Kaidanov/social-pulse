from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Hostage:
    id: str
    name: str
    age: int
    status: str
    location: Optional[str] = None
    capture_date: Optional[datetime] = None
    release_date: Optional[datetime] = None

@dataclass
class NewsUpdate:
    id: str
    title: str
    content: str
    source: str
    date: datetime 