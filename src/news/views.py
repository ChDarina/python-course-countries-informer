"""Представления Django"""
from typing import Any

from django.core.cache import caches
from django.db.models import QuerySet
from django.http import JsonResponse
from rest_framework import serializers
from rest_framework.decorators import api_view
from rest_framework.exceptions import NotFound
from rest_framework.request import Request
from rest_framework.settings import api_settings

from app.settings import CACHE_NEWS
from news.serializers import NewsSerializer
from news.services.news import NewsService

pagination_class = api_settings.DEFAULT_PAGINATION_CLASS
paginator = pagination_class()


def paginate(
        request: Request,
        serializer: serializers.ModelSerializer.__class__,
        data: QuerySet[Any],
):
    page = paginator.paginate_queryset(data, request)
    serializer = serializer(page, many=True)

    return paginator.get_paginated_response(serializer.data)


@api_view(["GET"])
def get_news(request: Request, alpha2code: str) -> JsonResponse:
    """
    Получение новостей для указанной страны.
    :param Request request: Объект запроса
    :param str alpha2code: ISO Alpha2 код страны
    :return:
    """

    cache_key = f"{alpha2code}_news"
    data = caches[CACHE_NEWS].get(cache_key)
    if not data:
        if data := NewsService().get_news(alpha2code):
            caches[CACHE_NEWS].set(cache_key, data)

    if data:
        return paginate(request, NewsSerializer, data)

    raise NotFound
