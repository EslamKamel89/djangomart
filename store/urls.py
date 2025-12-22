from django.urls import URLPattern, path

from . import views

urlpatterns: list[URLPattern] = [
    path("", views.HomeView.as_view()),
    path("products/<slug:slug>", views.ProductView.as_view(), name="product-view"),
    path("search/<slug:slug>/", views.CategoryView.as_view(), name="category-view"),
    path("product-form/", views.ProductFormView.as_view(), name="product-form"),
]
