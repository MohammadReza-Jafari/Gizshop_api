from rest_framework import generics, authentication, permissions, status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.settings import api_settings
from . import serializers


class SignupView(generics.CreateAPIView):
    serializer_class = serializers.UserSerializer


class GetAuthTokenView(ObtainAuthToken):
    serializer_class = serializers.AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

    def post(self, request, *args, **kwargs):
        ser = self.serializer_class(data=request.data, context={'request': request})

        if ser.is_valid(raise_exception=True):
            user = ser.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            return Response(
                {
                    'token': token.key,
                    'username': user.name,
                    'email': user.email
                },
                status=status.HTTP_200_OK
            )
        return Response(data=ser.errors, status=status.HTTP_401_UNAUTHORIZED)


class ManageUserView(generics.RetrieveUpdateAPIView):
    serializer_class = serializers.UserSerializer
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (authentication.TokenAuthentication,)

    def get_object(self):
        return self.request.user
