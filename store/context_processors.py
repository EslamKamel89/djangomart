from django.http import HttpRequest

from store.models import Category


def categories(request: HttpRequest):

    return {"categories": Category.objects.all()}
