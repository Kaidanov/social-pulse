from dataclasses import dataclass
from typing import List

@dataclass
class SocialMediaConfig:
    twitter_api_key: str
    twitter_api_secret: str
    instagram_api_key: str
    instagram_api_secret: str

@dataclass
class AppConfig:
    debug: bool = False
    data_sources: List[str] = ('csv', 'api', 'database')
    base_url: str = 'https://bringthemhome.org'
    social_media: SocialMediaConfig = None 