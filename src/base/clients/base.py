"""
Базовые функции для клиентов внешних сервисов.
"""

from abc import ABC, abstractmethod
from typing import Any, Optional

from http import HTTPStatus
import httpx
from app.settings import REQUESTS_TIMEOUT


class BaseClient(ABC):
    """
    Базовый класс, реализующий интерфейс для клиентов.
    """

    @abstractmethod
    def get_base_url(self) -> str:
        """
        Получение базового URL для запросов.

        :return:
        """

    def _request(self, endpoint: str) -> Optional[dict]:
        """
        Формирование и выполнение запроса.

        :param endpoint:
        :return:
        """
        with httpx.Client(timeout=REQUESTS_TIMEOUT) as client:
            headers: dict[str, Any] = {}
            params: dict[str, Any] = {}
            response = client.get(endpoint, headers=headers, params=params)
            if response.status_code == HTTPStatus.OK:
                return response.json()

            return None
