from django.urls import include, path
from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView, TokenVerifyView
)

from . import views

app_name = 'api'

urlpatterns = [
    path(
        'account/',
        include([
            path(
                '',
                views.AccountViewSet.as_view({
                    'get': 'retrieve',
                    'patch': 'partial_update',
                    'put': 'update',
                }),
            ),
            path(
                'signup/',
                views.AccountCreateView.as_view(),
            ),
            path(
                'login/',
                TokenObtainPairView.as_view(),
            ),
            path(
                'password-change/',
                views.AccountChangePasswordView.as_view(),
            ),
            path(
                'password-reset/',
                views.AccountPasswordResetView.as_view()
            ),
            path(
                'password-reset/<uidb64>/<token>/',
                views.AccountPasswordResetConfirmView.as_view(),
                name='password_reset_confirm'
            ),
            path(
                'refresh/',
                TokenRefreshView.as_view(),
            ),
            path(
                'verify/',
                TokenVerifyView.as_view(),
            ),
        ])
    ),
]
