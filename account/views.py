from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import UserSerializer, LoginSerializer

User = get_user_model()

class RegistrationView(APIView):
    def post(self, request):
        data = request.data
        serializer = UserSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response('Пользователь успешно зарегестрирован', status=201)



class ActivationView(APIView):
    def get(self, request):
        # data = request.data # request.POST
        # {'email': ...., 'activation_code': ....}
        # serializer = ActivationSerializer(data=data)
        # if serializer.is_valid(raise_excepetion=True):
        #     serializer.save()
        #     raise Response('Ваш аккаунт активирован', status=200)

        # email = data.get('email')
        # activation_code = data.get('activation_code')
        # try:
        #     user = User.objects.get(email=email, activation_code=activation_code)
        # except User.DoesNotExcist:
        #     return Response('Пользователь не найден', status=404)

        activation_code = request.query_params.get('u')
        user = get_object_or_404(User, activation_code=activation_code)
        user.is_active = True
        user.activation_code = ''
        user.save()
        return Response('Аккаунт успешно активирован', status=200)


class LoginView(ObtainAuthToken):
    serializer_class = LoginSerializer

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        #from rest_framework.authtoken.models import Token
        Token.objects.filter(user=user).delete()
        return Response('Вы успешно вышли', status=200)


class ResetPasswordView():
    pass

class ChangePasswordView():
    pass
