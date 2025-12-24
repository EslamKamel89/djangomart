from django.urls import URLPattern, path

from . import views

urlpatterns: list[URLPattern] = [
    path("register", views.RegisterView.as_view(), name="register")
]
