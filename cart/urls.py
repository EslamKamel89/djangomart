from django.urls import URLPattern, path

from . import views

urlpatterns: list[URLPattern] = [
    path("", views.CartShowCreateView.as_view(), name="cart-show-create"),
    path("<int:id>", views.CartUpdateDeleteView.as_view(), name="cart-update-delete"),
]
