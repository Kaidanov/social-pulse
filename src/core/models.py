from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Hostage:
    id: str
    name: str
    age: int
    status: str
    citizenship: str
    location: str
    capture_date: datetime
    details: str
    military_status: str
    image_url: Optional[str] = None
    local_image_path: Optional[str] = None
    days_in_captivity: Optional[int] = None
    age_group: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict) -> 'Hostage':
        """Create Hostage instance from dictionary"""
        return cls(
            id=data.get('id', ''),
            name=data.get('name', ''),
            age=int(data.get('age', 0)),
            status=data.get('status', ''),
            citizenship=data.get('citizenship', ''),
            location=data.get('location', ''),
            capture_date=datetime.strptime(data.get('capture_date', '2023-10-07'), '%Y-%m-%d'),
            details=data.get('details', ''),
            military_status=data.get('military_status', ''),
            image_url=data.get('image_url'),
            local_image_path=data.get('local_image_path'),
            days_in_captivity=data.get('days_in_captivity'),
            age_group=data.get('age_group')
        )

    def to_dict(self) -> dict:
        """Convert Hostage instance to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'status': self.status,
            'citizenship': self.citizenship,
            'location': self.location,
            'capture_date': self.capture_date.strftime('%Y-%m-%d'),
            'details': self.details,
            'military_status': self.military_status,
            'image_url': self.image_url,
            'local_image_path': self.local_image_path,
            'days_in_captivity': self.days_in_captivity,
            'age_group': self.age_group
        }

@dataclass
class NewsUpdate:
    id: str
    title: str
    content: str
    source: str
    date: datetime 