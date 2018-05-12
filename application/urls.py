from django.urls import path

from .views.user_management import (
    LoginView,
    CreateUserView,
)
from .views.general import IndexView
from .views.overtime_management import HandleOvertimeRequestView
from .views.report_management import ListDailyReports


user_management_paths = [
    path('login/', LoginView.as_view(), name='login'),
    path('create-user/', CreateUserView.as_view(), name='create-user'),
]

overtime_management_paths = [
    path('overtime-requests/',
         HandleOvertimeRequestView.as_view(),
         name='overtime-requests')
]

report_management_paths = [
    path('reports/', ListDailyReports.as_view(), name='report-list')
]

urlpatterns = [
    path('', IndexView.as_view(), name='index')
] + user_management_paths + overtime_management_paths + report_management_paths
