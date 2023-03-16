"""
Описание моделей данных (DTO).
"""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class NewsItemDTO(BaseModel):
    """
    Модель данных для новости.

    .. code-block::

        NewsItemDTO( source="BBC News", author="https://www.facebook.com/bbcnews", title="Ukraine war: China's claim
        to neutrality fades with Moscow visit", description="Beijing sees the Kremlin's war as serving a useful
        geopolitical purpose by confronting US influence.",
        url="https://www.bbc.co.uk/news/world-asia-china-64735707", published_at="2023-02-22T16:52:57Z", )
    """

    source: str
    author: Optional[str]
    title: str
    description: Optional[str]
    url: Optional[str]
    published_at: datetime
