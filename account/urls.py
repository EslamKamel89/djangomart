from django.urls import URLPattern, path

from . import views

urlpatterns: list[URLPattern] = [
    path("register", views.RegisterView.as_view(), name="register"),
    path(
        "email-verification",
        views.EmailVerification.as_view(),
        name="email-verification",
    ),
    path(
        "email-verification-sent",
        views.EmailVerificationSent.as_view(),
        name="email-verification-sent",
    ),
    path(
        "email-verification-success",
        views.EmailVerificationSuccess.as_view(),
        name="email-verification-success",
    ),
    path(
        "email-verification-failed",
        views.EmailVerificationFailed.as_view(),
        name="email-verification-failed",
    ),
]
