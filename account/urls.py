from django.contrib.auth import views as auth_views
from django.urls import URLPattern, path

from account.forms import CustomPasswordResetForm, CustomSetPasswordForm

from . import views

urlpatterns: list[URLPattern] = [
    path("login", views.LoginView.as_view(), name="login"),
    path("register", views.RegisterView.as_view(), name="register"),
    path("logout", views.LogoutView.as_view(), name="logout"),
    path("dashboard", views.DashboardView.as_view(), name="dashboard"),
    path(
        "dashboard/account-delete",
        views.AccountDeleteView.as_view(),
        name="account-delete",
    ),
    path(
        "dashboard/account-management",
        views.AccountManagementView.as_view(),
        name="account-management",
    ),
    path(
        "email-verification/<str:uidb64>/<str:token>",
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
    path(
        "password-reset/",
        auth_views.PasswordResetView.as_view(form_class=CustomPasswordResetForm),
        name="password_reset",
    ),
    path(
        "password-reset/done",
        auth_views.PasswordResetDoneView.as_view(),
        name="password_reset_done",
    ),
    path(
        "password-reset-confirm/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(form_class=CustomSetPasswordForm),
        name="password_reset_confirm",
    ),
    path(
        "password-reset-complete/",
        auth_views.PasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
]
