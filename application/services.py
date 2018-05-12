from django.contrib.auth import login
from django.http import HttpRequest

from application.models import User


def login_service(*, email: str, password: str, request: HttpRequest):
    user_qs = User.objects.filter(email=email)

    if user_qs.exists():
        user = user_qs.first()

        if user.check_password(password):
            login(request, user)

            return user

        return 'Could not authenticate with the provided credentials'


def create_user_service(*, email: str, password: str):
    if User.objects.filter(email=email).exists():
        return 'User already exists'

    return User.objects.create_user(email=email, password=password, is_active=True)
