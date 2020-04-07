import pytz
import logging
import datetime
from os import environ

from django.conf import settings
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets, permissions, mixins, generics
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.urls import reverse

from django_rest_passwordreset.signals import reset_password_token_created

from knox.models import AuthToken
from dotenv import load_dotenv
import mandrill

from .models import Entry, UserAuth
from .serializers import EntrySerializer, CreateUserSerializer, \
    UserSerializer, LoginUserSerializer


load_dotenv()

logger = logging.getLogger('vishnu.scheduler')
# pylint: disable=no-member

APP_HOSTNAME = environ.get("DEPLOYMENT_HOSTNAME")

# How long in days token will last before expiry, default value = 30 days
session_expiry = getattr(settings, "TOKEN_EXPIRY")
if (session_expiry is None or session_expiry == ''):
    session_expiry = 30


class ImmutableViewSet(mixins.CreateModelMixin,
                       mixins.ListModelMixin,
                       mixins.RetrieveModelMixin,
                       viewsets.GenericViewSet):
    """
    A viewset that provides `retrieve`, `create`, and `list` actions.

    To use it, override the class and set the `.queryset` and
    `.serializer_class` attributes.
    """


class EntryViewSet(ImmutableViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = EntrySerializer

    def get_queryset(self):
        user = self.request.user
        return Entry.objects.filter(owner=user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class RegistrationAPI(generics.GenericAPIView):
    serializer_class = CreateUserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        _, expires_in, link = self.generate_token_expiry_link(
            user)
        email_is_sent = self.send_email(user.email, link, expires_in)

        if email_is_sent:
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @staticmethod
    def generate_token_expiry_link(user):
        """
        Generates token and expiry, then generates link.
        Note that every time this a new token is generated, the `is_verified`
        attribute of `UserAuth` will be set to `False`.
        """

        EXPIRES_IN = 24  # hours
        expires_in_datetime = datetime.timedelta(hours=int(EXPIRES_IN))
        expiry = expires_in_datetime + datetime.datetime.now(tz=pytz.UTC)
        _, token = AuthToken.objects.create(user, expiry=expires_in_datetime)

        # Update or create accordingly
        user_auth, _ = UserAuth.objects.get_or_create(user=user)
        user_auth.token = token
        user_auth.expiry = expiry
        user_auth.is_verified = False
        user_auth.save()

        link = f"{APP_HOSTNAME}/api/auth/verify?email={user.email}&token={token}"

        return token, EXPIRES_IN, link

    @staticmethod
    def send_email(email, link, expires_in):

        try:
            mandrill_client = mandrill.Mandrill(
                environ.get('MANDRILL_API_KEY'))

            message = {'subject': "Verify your account",
                       'from_email': "noreply@aisingapore.org",
                       'from_name': "Tempcheck",
                       'html': "<p>Thank you for registering with us. " +
                       f"Click <a href='{link}'>here</a> " +
                       "to verify your account. Note that this link " +
                       f"will expire in {expires_in} hours.</p>",
                       "preserve_recipients": False}
            message["to"] = [{"email": email.strip()}]

            result = mandrill_client.messages.send(message)
            logger.info(f'Mandrill Results:\n{result}')
            logger.info('verification email sent')

        except mandrill.Error as error:
            logger.error(error)
            return False

        return True


class LoginAPI(generics.GenericAPIView):
    serializer_class = LoginUserSerializer

    def post(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data

        try:
            user_auth = UserAuth.objects.get(user=user)
        except ObjectDoesNotExist:
            logger.error("UserAuth object not found.")
            return Response(status=status.HTTP_404_NOT_FOUND)

        if not user_auth.is_verified:
            _, expiry, link = RegistrationAPI.generate_token_expiry_link(
                user)
            email_is_sent = RegistrationAPI.send_email(
                user.email, link, expiry)

            if email_is_sent:
                return Response(status=status.HTTP_205_RESET_CONTENT)
            else:
                return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        session_token = AuthToken.objects.create(
            user, expiry=datetime.timedelta(days=int(session_expiry)))[1]

        return Response({
            "user": UserSerializer(user,
                                   context=self.get_serializer_context()).data,
            # "token": AuthToken.objects.create(user)[1]
            "token": session_token,
            "expiry": datetime.timedelta(days=int(session_expiry)) + \
            datetime.date.today()
        }, status=status.HTTP_200_OK)


class UserAPI(generics.RetrieveAPIView):  # Same as baseview set later on
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class VerifyAPI(APIView):

    def get(self, request):
        """Checks if token is still valid and has not expired"""

        email = request.GET.get("email", "")
        token = request.GET.get("token", "")

        try:
            user = User.objects.get(username=email)
        except ObjectDoesNotExist:
            logger.error("User object not found.")
            return redirect("/#/serverError")

        try:
            user_auth = UserAuth.objects.get(user=user)
        except ObjectDoesNotExist:
            logger.error("UserAuth object not found.")
            return redirect("/#/serverError")

        if user_auth.is_verified:
            return redirect("/#/verified")
        elif datetime.datetime.now(tz=pytz.UTC) <= user_auth.expiry and \
                token == user_auth.token:
            user_auth.is_verified = True
            user_auth.save()
            return redirect("/#/verified")
        else:
            _, expiry, link = RegistrationAPI.generate_token_expiry_link(
                user)
            email_is_sent = RegistrationAPI.send_email(email, link, expiry)

            if email_is_sent:
                return redirect("/#/renewToken")
            else:
                return redirect("/#/serverError")


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    """
    Handles password reset tokens
    When a token is created, an e-mail needs to be sent to the user
    :param sender: View Class that sent the signal
    :param instance: View Instance that sent the signal
    :param reset_password_token: Token Model Object
    :param args:
    :param kwargs:
    :return:
    """
    # send an e-mail to the user
    context = {
        'current_user': reset_password_token.user,
        'username': reset_password_token.user.username,
        'email': reset_password_token.user.email,
        # 'reset_password_url': "{}?token={}".format(reverse('password_reset:reset-password-request'), reset_password_token.key),
        'reset_password_url': "/#/resetPassword?token={}".format(reset_password_token.key),
        'app_hostname': APP_HOSTNAME
    }

    # render email text
    email_html_message = render_to_string('email/user_reset_password.html', context)

    try:
        mandrill_client = mandrill.Mandrill(
            environ.get('MANDRILL_API_KEY'))

        message = {'subject': "Reset your Tempcheck password",
                   'from_email': "noreply@aisingapore.org",
                   'from_name': "Tempcheck",
                   'html': email_html_message,
                   "preserve_recipients": False}
        message["to"] = [{"email": reset_password_token.user.email}]

        result = mandrill_client.messages.send(message)
        logger.info(f'Mandrill Results:\n{result}')
        logger.info('verification email sent')

    except mandrill.Error as error:
        logger.error(error)
        return False

    return True