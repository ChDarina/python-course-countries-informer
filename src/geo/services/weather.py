from django.db.models import Q, QuerySet
from geo.clients.shemas import WeatherInfoDTO
from geo.clients.weather import WeatherClient
from geo.models import Weather
from geo.services.city import CityService


class WeatherService:
    """
    Сервис для работы с данными о погоде.
    """

    def get_weather(self, alpha2code: str, city: str) -> QuerySet[Weather]:
        """
        Получение погоды по локации.

        :param alpha2code: ISO Alpha2 код страны
        :param city: Город
        :return:
        """

        weather = Weather.objects.filter(
            Q(city__name__contains=city)
            | Q(city__country__alpha2code__contains=alpha2code)
        )

        if not weather:  # В БД еще нет данных о погоде по нужной локации
            if data := WeatherClient().get_weather(f"{city},{alpha2code}"):
                self.save_weather(data, city)
                weather = Weather.objects.filter(
                    Q(city__name__contains=city.capitalize())
                )
            return weather
        return weather

    @staticmethod
    def save_weather(weather: WeatherInfoDTO, city: str) -> Weather:
        """
        Формирование объекта модели погоды.

        :param CountryDTO weather: Данные о погоде
        :param str city: Город
        :return:
        """
        city = CityService().get_cities(city)[:1][0]
        return Weather.objects.create(
            city=city,
            temp=weather.temp,
            pressure=weather.pressure,
            humidity=weather.humidity,
            wind_speed=weather.wind_speed,
            description=weather.description,
            visibility=weather.visibility,
            dt=weather.dt,
            timezone=weather.timezone,
        )
