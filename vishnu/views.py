from rest_framework import viewsets, permissions, mixins, generics
from rest_framework.response import Response

import datetime

from knox.models import AuthToken

from .models import Entry
from django.conf import settings
from .serializers import EntrySerializer, CreateUserSerializer, UserSerializer, LoginUserSerializer
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
        token = AuthToken.objects.create(user, expiry=datetime.timedelta(days=int(expiry)))[1]
        
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            # "token": AuthToken.objects.create(user)[1]\
            "token": token,
            "expiry": datetime.timedelta(days=int(expiry)) + datetime.date.today()
        })

class LoginAPI(generics.GenericAPIView):
    serializer_class = LoginUserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        token = AuthToken.objects.create(user, expiry=datetime.timedelta(days=int(expiry)))[1]

        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            # "token": AuthToken.objects.create(user)[1]
            "token": token,
            "expiry": datetime.timedelta(days=int(expiry)) + datetime.date.today()
        })

class UserAPI(generics.RetrieveAPIView): # Same as baseview set later on
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user
