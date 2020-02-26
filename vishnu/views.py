import pytz
import logging
import datetime
from os import environ

from django.conf import settings
from django.shortcuts import redirect
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, permissions, mixins, generics

from knox.models import AuthToken
from knox.auth import TokenAuthentication
from dotenv import load_dotenv
import mandrill

from .settings import DEBUG
from .models import Entry, UserAuth
from .serializers import EntrySerializer, CreateUserSerializer, \
    UserSerializer, LoginUserSerializer


load_dotenv()

logger = logging.getLogger('vishnu.scheduler')
# pylint: disable=no-member

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

        session_token = AuthToken.objects.create(
            user, expiry=datetime.timedelta(days=int(session_expiry)))[1]

        _, expires_in, link = self.generate_token_expiry_link(
            user)
        self.send_email(user.email, link, expires_in)

        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": session_token
        })

    @staticmethod
    def generate_token_expiry_link(user):
        """Generates token and expiry, then generates link"""

        EXPIRES_IN = 1  # minute

        expires_in_datetime = datetime.timedelta(minutes=int(EXPIRES_IN))
        expiry = expires_in_datetime + datetime.datetime.now(tz=pytz.UTC)

        _, token = AuthToken.objects.create(user, expiry=expires_in_datetime)

        # TODO serialize this
        # TODO use knox's model
        # Update and create accordingly
        userauth_queryset = UserAuth.objects.filter(user=user)
        if userauth_queryset.count() == 0:
            user_auth = UserAuth(user=user, token=token, expiry=expiry)
            user_auth.save()
        else:
            user_auth = userauth_queryset[0]
            user_auth.token = token
            user_auth.expiry = expiry
            user_auth.is_verified = False
            user_auth.save()

        if DEBUG:
            hostname = "127.0.0.1:8000"
            link = f"http://{hostname}/api/auth/verify?email={user.email}&token={token}"
        else:
            hostname = environ.get("DEPLOYMENT_HOSTNAME")
            link = f"https://{hostname}/api/auth/verify?email={user.email}&token={token}"

        return token, EXPIRES_IN, link

    @staticmethod
    def send_email(email, link, expires_in):

        if DEBUG:
            email = environ.get("TEST_VERIFY_EMAIL")

        try:
            mandrill_client = mandrill.Mandrill(
                environ.get('MANDRILL_API_KEY'))

            message = {'subject': "Verify your account",
                       'from_email': "noreply@aisingapore.org",
                       'from_name': "LOA",
                       'html': "<p>Hey, " +
                       f"click <a href='{link}'>here</a> " +
                       "to verify your account. " +
                       f"Note that this link will expire in {expires_in} hours.</p>",
                       "preserve_recipients": False}
            message["to"] = [{"email": email.strip()}]

            result = mandrill_client.messages.send(message)
            logger.info(f'Mandrill Results:\n{result}')
            logger.info('verification email sent')
        except mandrill.Error as error:
            logger.error(error)


class LoginAPI(generics.GenericAPIView):
    serializer_class = LoginUserSerializer

    def post(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data

        session_token = AuthToken.objects.create(
            user, expiry=datetime.timedelta(days=int(session_expiry)))[1]

        userauth_queryset = UserAuth.objects.filter(user=user)
        if userauth_queryset.count() == 0:
            return Response({"token": ""})
        else:

            user_auth = userauth_queryset[0]
            if not user_auth.is_verified:
                # Regenerate token
                _, expiry, link = RegistrationAPI.generate_token_expiry_link(
                    user)
                RegistrationAPI.send_email(user.email, link, expiry)

                return Response({"token": ""})

        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            # "token": AuthToken.objects.create(user)[1]
            "token": session_token,
            "expiry": datetime.timedelta(days=int(session_expiry)) + datetime.date.today()
        })


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

        # TODO handle no such user/email (unlikely)
        user = User.objects.filter(username=email)[0]

        # TODO handle no user_auth
        user_auth = UserAuth.objects.filter(user=user)[0]

        if user_auth.is_verified:
            return redirect("/#/verified")
        elif datetime.datetime.now(tz=pytz.UTC) <= user_auth.expiry and \
                token == user_auth.token:
            user_auth.is_verified = True
            user_auth.save()
            return redirect("/#/verified")
        else:
            # Regenerate token
            _, expiry, link = RegistrationAPI.generate_token_expiry_link(
                user)
            RegistrationAPI.send_email(email, link, expiry)

            return redirect("/#/expired")
