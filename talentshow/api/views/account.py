from django.core.exceptions import ValidationError
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_decode
from django.utils.translation import gettext_lazy as _
from rest_framework import (
    mixins, permissions, response, status, views, viewsets
)

from .. import serializers
from core import constants

UserModel = get_user_model()


class AccountViewSet(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet
):
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = serializers.AccountSerializer
    model = UserModel

    def get_object(self):
        return self.request.user

#For no type accounts
class AccountCreateView(views.APIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = serializers.AccountCreateSerializer

    def get_serializer_class(self):
        return self.serializer_class

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer_class()(data=request.data)
        serializer.is_valid(raise_exception=True)
        return self.serializer_valid(serializer)

    def serializer_valid(self, serializer):
        serializer.save(validated_data=serializer.validated_data)
        return response.Response({
            'detail': _("Account created.")
        })


class AccountChangePasswordView(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = serializers.PasswordChangeSerializer

    def get_serializer_class(self):
        return self.serializer_class

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer_class()(
            user=request.user, data=request.data
        )
        serializer.is_valid(raise_exception=True)
        return self.serializer_valid(serializer)

    def serializer_valid(self, serializer):
        serializer.save(validated_data=serializer.validated_data)
        return response.Response({
            'detail': _("Password updated.")
        })


class AccountPasswordResetView(views.APIView):
    extra_email_context = None
    email_template_name = 'registration/password_reset_email.html'
    from_email = None
    html_email_template_name = None
    permission_classes = (
        permissions.AllowAny,
    )
    serializer_class = serializers.PasswordResetSerializer
    subject_template_name = 'registration/password_reset_subject.txt'
    token_generator = default_token_generator

    def get_serializer_class(self):
        return self.serializer_class

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer_class()(data=request.data)
        serializer.is_valid(raise_exception=True)
        return self.serializer_valid(serializer)

    def serializer_valid(self, serializer):
        domain = self.request.META['HTTP_REFERER']
        domain = domain \
            .replace('http://', '') \
            .replace('https://', '') \
            .replace('/', '')

        opts = {
            'domain_override': domain,
            'email_template_name': self.email_template_name,
            'extra_email_context': self.extra_email_context,
            'from_email': self.from_email,
            'html_email_template_name': self.html_email_template_name,
            'request': self.request,
            'subject_template_name': self.subject_template_name,
            'token_generator': self.token_generator,
            'use_https': self.request.is_secure(),
        }
        serializer.save(validated_data=serializer.validated_data, **opts)
        return response.Response({
            'detail': _(
                "We've emailed you instructions for setting your password,"
                " if an account exists with the email you entered. You "
                "should receive them shortly."
            )
        })


class AccountPasswordResetConfirmView(views.APIView):
    permission_classes = (
        permissions.AllowAny,
    )
    post_reset_login = False
    post_reset_login_backend = None
    serializer_class = serializers.SetPasswordSerializer
    token_generator = default_token_generator

    def get(self, request, *args, **kwargs):
        assert 'uidb64' in kwargs and 'token' in kwargs

        self.user = self.get_user(kwargs['uidb64'])
        if self.user is not None:
            token = kwargs['token']
            if self.token_generator.check_token(self.user, token):
                return response.Response(status=status.HTTP_204_NO_CONTENT)

        return response.Response(status=status.HTTP_401_UNAUTHORIZED)

    def post(self, request, *args, **kwargs):
        assert 'uidb64' in kwargs and 'token' in kwargs

        self.user = self.get_user(kwargs['uidb64'])

        if self.user is not None:
            token = kwargs['token']
            if self.token_generator.check_token(self.user, token):
                serializer = self.serializer_class(
                    user=self.user, data=request.data
                )
                serializer.is_valid(raise_exception=True)
                return self.serializer_valid(serializer)

        return response.Response(status=status.HTTP_401_UNAUTHORIZED)

    def get_user(self, uidb64):
        try:
            # urlsafe_base64_decode() decodes to bytestring
            uid = urlsafe_base64_decode(uidb64).decode()
            user = UserModel._default_manager.get(pk=uid)
        except (
            TypeError,
            ValueError,
            OverflowError,
            UserModel.DoesNotExist,
            ValidationError
        ):
            user = None
        return user

    def serializer_valid(self, serializer):
        serializer.save(validated_data=serializer.validated_data)
        return response.Response({
            'detail': _(
                "Your password has been set.  You may go ahead and log in now."
            )
        })
