from typing import Any

from django.db.models.query import QuerySet
from django.http import HttpRequest
from django.shortcuts import render
from django.views.generic import DetailView, ListView, TemplateView, View


class CartShowCreateView(View):
    def get(self, request: HttpRequest):
        pass

    def post(self, request: HttpRequest):
        pass


class CartUpdateDeleteView(View):
    def put(self, request: HttpRequest, id: int):
        pass

    def delete(self, request: HttpRequest, id: int):
        pass
