from django.db.models import Q, QuerySet
from geo.clients.currency import CurrencyClient
from geo.models import CurrencyRates
from geo.models import Currency


class CurrencyService:
    """
    Сервис для работы с данными о валюте.
    """

    def get_currency(self, base: str = "rub") -> QuerySet[CurrencyRates]:
        """
        Получение курса валют по базовой валюте.

        :param base: Название базовой валюты
        :return:
        """

        currency_rates = CurrencyRates.objects.filter(Q(currency__base__contains=base))

        if not currency_rates:  # В БД еще нет курсов валют для искомой валюты
            if data := CurrencyClient().get_currency(base):
                # Сохранение в БД новых данных
                currency = Currency.objects.create(
                    base=data.base,
                    date=data.date,
                )
                self.save_rates(currency, data.rates)

                currency_rates = CurrencyRates.objects.filter(
                    Q(currency__base__contains=currency.base)
                )
        return currency_rates

    @staticmethod
    def save_rates(currency: Currency, rates: dict) -> None:
        CurrencyRates.objects.bulk_create(
            [
                CurrencyService.build_model(currency, name, rate)
                for name, rate in rates.items()
            ],
            batch_size=1000,
        )

    @staticmethod
    def save_currency(base: str, date: str) -> Currency:
        return Currency.objects.create(
            base=base,
            date=date,
        )

    @staticmethod
    def build_model(currency: Currency, name: str, rate: float) -> CurrencyRates:
        """
        Формирование объекта модели валюты.

        :param CurrencyRatesDTO currency: Данные о валюте.
        :param str name: Имя валюты.
        :param float rate: Валютный курс.
        :return:
        """

        return CurrencyRates(
            currency=currency,
            currency_name=name,
            rate=rate,
        )
