import logging
from datetime import datetime

from django.urls import reverse
from geo.models import Country
from news.models import News
from rest_framework.test import APITestCase

logger = logging.getLogger()


class NewsTestCase(APITestCase):
    """
    Класс тестов для информации о новостях.
    """

    def setUp(self) -> None:
        """
        Инициализация данных.
        :return:
        """
        self.country = Country.objects.create(
            name="Russia",
            alpha2code="ru",
            alpha3code="rus",
            capital="Moscow",
            region="Europe",
            subregion="Northern Europe",
            population=0,
            latitude=0,
            longitude=0,
            demonym="test",
            area=0,
            numeric_code=1,
            flag="",
            currencies=[],
            languages=[],
        )
        self.news = [
            News.objects.create(
                country=self.country,
                source="BBC",
                author="author1",
                title="some news",
                description="",
                url="example.com",
                published_at=datetime.now().astimezone(),
            ),
            News.objects.create(
                country=self.country,
                source="Google",
                author="author2",
                title="another news",
                description="smth there",
                url="www.example.com",
                published_at=datetime.now().astimezone(),
            ),
        ]

    def test_get_news(self) -> None:
        """
        Тест получения новостей.
        :return:
        """
        response = self.client.get(
            reverse("news", kwargs={"alpha2code": self.country.alpha2code})
        )
        data = response.json()['results']
        logger.info(data)
        self.assertEqual(len(data), 1)
        news = data[0]
        self.assertEqual(news["country"]["name"], self.news[0].country.name)
        self.assertEqual(news["source"], self.news[0].source)
        self.assertEqual(news["author"], self.news[0].author)
        self.assertEqual(news["title"], self.news[0].title)
        self.assertEqual(news["description"], self.news[0].description)
        self.assertEqual(news["url"], self.news[0].url)
