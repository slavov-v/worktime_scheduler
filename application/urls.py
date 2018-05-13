from django.urls import path

from .views.user_management import (
    LoginView,
    CreateUserView,
    EditPersonalDataView,
    LogOutView
)
from .views.general import IndexView, CreateTicketView, AddAvailabilityView, TrackDailyWorktimeView
from .views.overtime_management import HandleOvertimeRequestView, RequestOvertimeView
from .views.report_management import ListDailyReports, CreateReportView


user_management_paths = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogOutView.as_view(), name='logout'),
    path('create-user/', CreateUserView.as_view(), name='create-user'),
    path('edit-personal-data', EditPersonalDataView.as_view(), name='edit-personal-data')
]

overtime_management_paths = [
    path('overtime-requests/',
         HandleOvertimeRequestView.as_view(),
         name='overtime-requests'),
    path('request-overtime/', RequestOvertimeView.as_view(), name='request-overtime')
]

report_management_paths = [
    path('reports/', ListDailyReports.as_view(), name='report-list'),
    path('create-report/', CreateReportView.as_view(), name='create-report'),
    path('add-availability/', AddAvailabilityView.as_view(), name='add-availability'),
    path('track-worktime/', TrackDailyWorktimeView.as_view(), name='track-worktime')
]

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('create-ticket/', CreateTicketView.as_view(), name='create-ticket')
] + user_management_paths + overtime_management_paths + report_management_paths
