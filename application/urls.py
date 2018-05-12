from django.urls import path

from .views.user_management import LoginView, CreateUserView
from .views.general import IndexView


user_management_paths = [
    path('login/', LoginView.as_view(), name='login'),
    path('create-user/', CreateUserView.as_view(), name='create-user')
]

urlpatterns = [
    path('', IndexView.as_view(), name='index')
] + user_management_paths
