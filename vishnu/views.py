from os import environ
import datetime
import pytz
import logging

from django.conf import settings
from django.shortcuts import redirect
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, permissions, mixins, generics

from knox.models import AuthToken
from knox.auth import TokenAuthentication
from dotenv import load_dotenv
import mandrill

from .models import Entry, UserAuth
from .serializers import EntrySerializer, CreateUserSerializer, \
    UserSerializer, LoginUserSerializer
from .settings import DEBUG


load_dotenv()

logger = logging.getLogger('vishnu.scheduler')
# pylint: disable=no-member

# How long in days token will last before expiry, default value = 30 days
expiry = getattr(settings, "TOKEN_EXPIRY")
if (expiry is None or expiry == ''):
    expiry = 30


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
        token = AuthToken.objects.create(
            user, expiry=datetime.timedelta(days=int(expiry)))[1]

        verification_link = self.get_verification_link(user)
        if DEBUG:
            self.send_email(name="Raimi", email="raimi.bkarim@gmail.com",
                            verification_link=verification_link)
        else:
            self.verify_email(name="Raimi", email=user.email,
                              verification_link=verification_link)

        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            # "token": AuthToken.objects.create(user)[1]\
            # "token": token,
            # "expiry": datetime.timedelta(days=int(expiry)) + datetime.date.today()
        })

    def get_verification_link(self, user):

        EXPIRES_IN = 1  # MINUTES

        token = AuthToken.objects.create(
            user, expiry=datetime.timedelta(minutes=int(EXPIRES_IN)))[1]
        expiry = datetime.timedelta(minutes=int(
            EXPIRES_IN)) + datetime.datetime.now()

        user_auth = UserAuth(user=user, token=token, expiry=expiry)
        user_auth.save()

        if DEBUG:
            return f"http://127.0.0.1:8000/api/auth/verify?email={user.email}&token={token}"
        else:
            return f"https://loa.ai3.aisingapore.org//api/auth/verify?email={user.email}&token={token}"

    def send_email(self, name, email, verification_link):

        try:
            mandrill_client = mandrill.Mandrill(
                environ.get('MANDRILL_API_KEY'))

            message = {'subject': "Verify your account",
                       'from_email': "noreply@aisingapore.org",
                       'from_name': "LOA",
                       'html': f"<p>Hey {name}, " +
                       f"click <a href='{verification_link}'>here</a>" +
                       " to verify your account. Note: this link will expire in 48 hours.</p>",
                       'preserve_recipients': False}
            message['to'] = [{'email': email.strip(), 'name': name.strip()}]

            result = mandrill_client.messages.send(message)
            logger.info(f'Mandrill Results:\n{result}')
            logger.info('report sent')
        except mandrill.Error as error:
            logger.error(error)


class LoginAPI(generics.GenericAPIView):
    serializer_class = LoginUserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        token = AuthToken.objects.create(
            user, expiry=datetime.timedelta(days=int(expiry)))[1]

        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            # "token": AuthToken.objects.create(user)[1]
            "token": token,
            "expiry": datetime.timedelta(days=int(expiry)) + datetime.date.today()
        })


class UserAPI(generics.RetrieveAPIView):  # Same as baseview set later on
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class VerifyAPI(APIView):
    # authentication_classes = [TokenAuthentication, ]
    # permission_classes = [IsAuthenticated, ]

    def get(self, request):
        email = request.GET.get('email', '')
        token = request.GET.get('token', '')

        user = User.objects.filter(username=email)[0]
        user_auth = UserAuth.objects.filter(user=user)[0]

        if datetime.datetime.now(tz=pytz.UTC) <= user_auth.expiry and \
                user_auth.token == token:
            return redirect("/#/verified")

        return redirect("/#/expired")
