from django import forms

from application.models import User


class CredentialsForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())


class RequestOvertimeForm(forms.Form):
    date = forms.DateField()
    employer = forms.ModelChoiceField(queryset=User.objects.filter(is_superuser=True))


class EditPersonalDataForm(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()


class CreateReportForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea())


class CreateTicketForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea())


class AddAvailabilityForm(forms.Form):
    date = forms.DateTimeField(widget=forms.SelectDateWidget())
