from django.contrib.auth import password_validation
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import _unicode_ci_compare
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMultiAlternatives
from django.template import loader
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers


UserModel = get_user_model()


class AccountSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(max_length=150)
    last_name = serializers.CharField(max_length=150)

    class Meta:
        fields = (
            'email', 'first_name', 'last_name', 'company_name',
            'company_category', 'phone_number', 'language', 'timezone'
        )
        model = UserModel
        read_only_fields = ('email', )

#For general type accounts
class AccountCreateSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password1 = serializers.CharField(
        trim_whitespace=False,
        style={'input_type': 'password'}
    )
    password2 = serializers.CharField(
        trim_whitespace=False,
        style={'input_type': 'password'}
    )
    first_name = serializers.CharField(max_length=150)
    last_name = serializers.CharField(max_length=150)

    class Meta:
        fields = (
            'email', 'password1', 'password2', 'first_name', 'last_name', 
            'company_name', 'company_category', 'phone_number', 'language',
        )
        model = UserModel

    def validate(self, data):
        password1 = data.get('password1')
        password2 = data.get('password2')
        if password1 and password2:
            if password1 != password2:
                raise serializers.ValidationError(
                    _("The two password fields didn't match."),
                )
        password_validation.validate_password(password2)
        return data

    def validate_email(self, value):
        qs = UserModel._default_manager.filter(email__iexact=value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError(
                _('A user with that email already exists.')
            )
        return value

    def save(self, validated_data):
        user = UserModel._default_manager.create_user(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
        )
        user.set_password(validated_data['password1'])
        user.save()
        return user


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def get_users(self, email):
        email_field_name = UserModel.get_email_field_name()
        active_users = UserModel._default_manager.filter(
            **{
                '%s__iexact' % UserModel.get_email_field_name(): email,
                'is_active': True,
            }
        )
        return (
            u
            for u in active_users
            if u.has_usable_password()
            and _unicode_ci_compare(email, getattr(u, email_field_name))
        )

    def save(
        self,
        validated_data,
        domain_override=None,
        subject_template_name='registration/password_reset_subject.txt',
        email_template_name='registration/password_reset_email.html',
        use_https=False,
        token_generator=default_token_generator,
        from_email=None,
        request=None,
        html_email_template_name=None,
        extra_email_context=None
    ):
        email = validated_data['email']
        if not domain_override:
            current_site = get_current_site(request)
            site_name = current_site.name
            domain = current_site.domain
        else:
            site_name = domain = domain_override
        email_field_name = UserModel.get_email_field_name()
        for user in self.get_users(email):
            user_email = getattr(user, email_field_name)
            context = {
                'email': user_email,
                'domain': domain,
                'site_name': site_name,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'user': user,
                'token': token_generator.make_token(user),
                'protocol': 'https' if use_https else 'http',
                **(extra_email_context or {}),
            }
            self.send_mail(
                subject_template_name,
                email_template_name,
                context,
                from_email,
                user_email,
                html_email_template_name=html_email_template_name,
            )

    def send_mail(
        self,
        subject_template_name,
        email_template_name,
        context,
        from_email,
        to_email,
        html_email_template_name=None
    ):
        subject = loader.render_to_string(subject_template_name, context)
        # Email subject *must not* contain newlines
        subject = ''.join(subject.splitlines())
        body = loader.render_to_string(email_template_name, context)

        email_message = EmailMultiAlternatives(
            subject, body, from_email, [to_email])
        if html_email_template_name is not None:
            html_email = loader.render_to_string(
                html_email_template_name, context)
            email_message.attach_alternative(html_email, 'text/html')

        email_message.send()


class SetPasswordSerializer(serializers.Serializer):
    new_password1 = serializers.CharField(style={'input_type': 'password'})
    new_password2 = serializers.CharField(style={'input_type': 'password'})

    def __init__(self, user=None, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def validate(self, data):
        password1 = data.get('new_password1')
        password2 = data.get('new_password2')
        if password1 and password2:
            if password1 != password2:
                raise serializers.ValidationError(
                    _("The two password fields didn't match."),
                )
        password_validation.validate_password(password2, self.user)
        return data

    def save(self, validated_data):
        password = validated_data["new_password1"]
        self.user.set_password(password)
        self.user.save()
        return self.user


class PasswordChangeSerializer(SetPasswordSerializer):
    old_password = serializers.CharField(style={'input_type': 'password'})

    def validate_old_password(self, data):
        old_password = data
        if not self.user.check_password(old_password):
            raise serializers.ValidationError(
                _(
                    "Your old password was entered incorrectly. "
                    "Please enter it again."
                )
            )
        return old_password
