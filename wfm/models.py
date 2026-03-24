from datetime import datetime
from typing import List, Optional, Dict
from pydantic import BaseModel, Field

class UserActivity(BaseModel):
    type: str
    details: Optional[str] = None

class User(BaseModel):
    id: str
    ingame_name: str = Field(alias="ingameName")
    slug: str
    avatar: Optional[str] = None
    reputation: int
    platform: str
    crossplay: bool = False
    locale: str
    status: str
    activity: Optional[UserActivity] = None
    last_seen: Optional[datetime] = Field(default=None, alias="lastSeen")

class Order(BaseModel):
    id: str
    type: str
    platinum: int
    quantity: int
    per_trade: int = Field(default=1, alias="perTrade")
    rank: Optional[int] = None
    visible: bool
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    item_id: str = Field(alias="itemId")
    user: User

class ItemI18nDetail(BaseModel):
    name: str
    description: str
    wiki_link: Optional[str] = Field(default=None, alias="wikiLink")
    icon: str
    thumb: str

class Item(BaseModel):
    id: str
    slug: str
    game_ref: Optional[str] = Field(default=None, alias="gameRef")
    tags: List[str] = []
    rarity: Optional[str] = None
    bulk_tradable: bool = Field(default=False, alias="bulkTradable")
    max_rank: Optional[int] = Field(default=None, alias="maxRank")
    trading_tax: Optional[int] = Field(default=None, alias="tradingTax")
    tradable: bool = True
    i18n: Dict[str, ItemI18nDetail]