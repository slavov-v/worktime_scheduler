from django.urls import path

from .views.user_management import (
    LoginView,
    CreateUserView,
    EditPersonalDataView,
    LogOutView,
    DeleteUserView
)
from .views.general import (
    IndexView,
    CreateTicketView,
    AddAvailabilityView,
    TrackDailyWorktimeView,
    UserStatusList,
    EditUserWorkDataView,
    CalculateSalaryView,
    UserWorkHistoryView,
    CheckUserDataView,
    CalculateVacationView
)
from .views.overtime_management import HandleOvertimeRequestView, RequestOvertimeView
from .views.report_management import ListDailyReports, CreateReportView, CreateReportCommentView


user_management_paths = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogOutView.as_view(), name='logout'),
    path('create-user/', CreateUserView.as_view(), name='create-user'),
    path('delete-user/<int:user_id>/', DeleteUserView.as_view(), name='delete-user'),
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
    path('create-report-comment/', CreateReportCommentView.as_view(), name='create-report-comment')
]

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('create-ticket/', CreateTicketView.as_view(), name='create-ticket'),
    path('add-availability/', AddAvailabilityView.as_view(), name='add-availability'),
    path('track-worktime/', TrackDailyWorktimeView.as_view(), name='track-worktime'),
    path('user-statuses/', UserStatusList.as_view(), name='user-status-list'),
    path('edit-work-data/<int:user_id>/', EditUserWorkDataView.as_view(), name='edit-user-work-data'),
    path('calculate-salary/<int:user_id>/', CalculateSalaryView.as_view(), name='calculate-salary'),
    path('work-history/<int:user_id>/', UserWorkHistoryView.as_view(), name='user-work-history'),
    path('check-user-data/<int:user_id>/', CheckUserDataView.as_view(), name='check-user-data'),
    path('calculate-vacation/<int:user_id>/', CalculateVacationView.as_view(), name='calculate-vacation')
] + user_management_paths + overtime_management_paths + report_management_paths
