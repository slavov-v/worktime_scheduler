from django import forms

from application.models import User, Report


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


class EditUserWorkDataForm(forms.Form):
    position = forms.ChoiceField(choices=User.POSITION_CHOICES)
    hour_salary = forms.FloatField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['position'].widget.attrs['class'] = 'form-control'


class CreateReportCommentForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea)
    report = forms.ModelChoiceField(queryset=Report.objects.all())


class SendEmailForm(forms.Form):
    subject = forms.CharField()
    content = forms.CharField(widget=forms.Textarea)
    to = forms.EmailField()
