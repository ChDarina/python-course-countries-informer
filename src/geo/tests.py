from datetime import datetime
from typing import List

from django.urls import reverse
from geo.models import City, Country, Currency, CurrencyRates, Weather
from rest_framework.test import APITestCase


class TestData:
    """
    Класс с созданием данных для тестов.
    """

    @staticmethod
    def test_country() -> Country:
        """
        Создание страны.
        :return:
        """
        return Country.objects.create(
            name="Test name",
            alpha2code="te",
            alpha3code="tes",
            capital="capital",
            region="Test region",
            subregion="Test subregion",
            population=100000,
            latitude=0,
            longitude=0,
            demonym="Test demonym",
            area=10000,
            numeric_code=0,
            flag="Test flag",
            currencies=[],
            languages=["Test lang"],
        )

    @staticmethod
    def test_city(country: Country) -> City:
        """
        Создание города.
        :return:
        """
        return City.objects.create(
            country=country,
            name="name",
            region="Test region",
            latitude=10,
            longitude=10,
        )

    @staticmethod
    def test_weather(city: City) -> Weather:
        """
        Создание погоды.
        :return:
        """
        return Weather.objects.create(
            city=city,
            temp=10,
            pressure=10000,
            humidity=70,
            wind_speed=10,
            description="sunny",
            visibility=10000,
            dt=datetime.now().astimezone(),
            timezone=5,
        )

    @staticmethod
    def test_currency() -> Currency:
        """
        Создание валюты.
        :return:
        """
        return Currency.objects.create(base="rub", date=datetime.now().astimezone())

    @staticmethod
    def test_currency_rates(currency: Currency) -> List[CurrencyRates]:
        """
        Создание валютного курса.
        :return:
        """
        return [CurrencyRates.objects.create(currency=currency, currency_name="eur", rate=40.0)]


class CountryTest(APITestCase):
    """
    Класс тестов для стран.
    """

    def setUp(self) -> None:
        """
        Инициализация страны.
        :return:
        """
        self.country = TestData.test_country()

    def test_get_countries(self) -> None:
        """
        Тест получения списка стран.
        :return:
        """
        response = self.client.get(
            reverse("countries"), {"codes": self.country.alpha2code}
        )
        data = response.json()["results"]
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["name"], self.country.name)

    def test_get_country(self) -> None:
        """
        Тест получения одной страны.
        :return:
        """
        response = self.client.get(
            reverse("country", kwargs={"name": self.country.name})
        )
        data = response.json()["results"][0]
        self.assertEqual(data["name"], self.country.name)


class CityTest(APITestCase):
    """
    Класс тестов для городов.
    """

    def setUp(self) -> None:
        """
        Инициализация города.
        :return:
        """
        self.country = TestData.test_country()
        self.city = TestData.test_city(self.country)

    def test_get_cities(self) -> None:
        """
        Тест получения списка городов.
        :return:
        """
        response = self.client.get(reverse("cities"), {"codes": "te,name"})
        data = response.json()['results']
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["name"], self.city.name)
        self.assertEqual(data[0]["country"]["name"], self.city.country.name)

    def test_get_city(self) -> None:
        """
        Тест получения одного города.
        :return:
        """
        response = self.client.get(reverse("city", kwargs={"name": self.city.name}))
        data = response.json()["results"][0]
        self.assertEqual(data["name"], self.city.name)


class CurrencyTest(APITestCase):
    """
    Класс тестов для валют.
    """

    def setUp(self) -> None:
        """
        Инициализация валюты.
        :return:
        """
        self.currency = TestData.test_currency()
        self.currency_rates = TestData.test_currency_rates(self.currency)

    def test_get_currency(self) -> None:
        """
        Тест получения валютного курса.
        :return:
        """
        data = self.client.get(reverse("currency", kwargs={"base": "rub"})).json()['results']
        self.assertEqual(len(data), 1)
        for i, item in enumerate(data):
            self.assertEqual(item["currency_name"], self.currency_rates[i].currency_name)
            self.assertEqual(item["rate"], self.currency_rates[i].rate)


class WeatherTest(APITestCase):
    """
    Класс тестов для погоды.
    """

    def setUp(self) -> None:
        """
        Инициализация погоды.
        :return:
        """
        self.country = TestData.test_country()
        self.city = TestData.test_city(self.country)
        self.weather = TestData.test_weather(self.city)

    def test_get_weather(self) -> None:
        """
        Тест получения погоды.
        :return:
        """
        data = self.client.get(
            reverse(
                "weather",
                kwargs={"alpha2code": self.country.alpha2code, "city": self.city.name},
            )
        ).json()['results'][0]
        self.assertEqual(data["temp"], self.weather.temp)
        self.assertEqual(data["pressure"], self.weather.pressure)
        self.assertEqual(data["humidity"], self.weather.humidity)
        self.assertEqual(data["wind_speed"], self.weather.wind_speed)
        self.assertEqual(data["description"], self.weather.description)
        self.assertEqual(data["visibility"], self.weather.visibility)
        self.assertEqual(data["timezone"], self.weather.timezone)
