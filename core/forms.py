import datetime
from django import forms
from django.contrib.auth.models import User
from allauth.account.forms import LoginForm as AllauthLoginForm, SignupForm, ResetPasswordForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Div, Field, Row, Column
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils import timezone
from .models import Reservation, BikeInstance
from django.db.models import Q


class CrispyResetPasswordForm(ResetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.form_action = reverse("account_reset_password")
        self.helper.form_show_errors = True
        self.helper.error_text_inline = True
        self.helper.help_text_inline = False
        self.fields["email"].label = ""
        self.fields["email"].widget.attrs.update({
            "required": True,
            "id": "email",
            "type": "email",
            "class": "input-form",
            "placeholder": "Email",
            "autocomplete": "email",
        })
        self.helper.layout = Layout(
            'email',
            Div(
                Submit("submit", "Reset password", css_class="btn btn-success"),
                css_class="d-flex justify-content-center my-4")
        )

class LoginForm(AllauthLoginForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.form_action = reverse("account_login")
        self.helper.form_show_errors = True
        self.helper.error_text_inline = True
        self.helper.help_text_inline = False
        self.fields["login"].label = ""
        self.fields["login"].widget.attrs.update({
            "required": True,
            "id": "username",
            "class": "input-form",
            "placeholder": "Username/Email",
            "autocomplete": "username",
        })
        self.fields["password"].label = ""
        self.fields["password"].widget.attrs.update({
            "required": True,
            "id": "password",
            "type": "password",
            "class": "input-form",
            "placeholder": "Password",
            "autocomplete": "current-password",
        })
        self.helper.layout = Layout(
            'login',
            'password',
            Div(
                Submit("submit", "Login", css_class="btn btn-success"),
                css_class="d-flex justify-content-center my-4")
        )


class RegistrationForm(SignupForm):
    terms_of_service = forms.BooleanField(
        label= mark_safe("I agree to the <a href='/terms/' class='terms-text fw-bold text-body'>Terms of Service</a>"),
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'terms_of_service']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.form_action = reverse("account_signup")
        self.helper.form_show_errors = True
        self.helper.error_text_inline = True
        self.helper.help_text_inline = False

        self.fields["username"].help_text = ""
        self.fields["username"].label = ""
        self.fields["username"].widget.attrs.update({
            "required": True,
            "name": "username",
            "id": "username",
            "type": "text",
            "class": "input-form",
            "placeholder": "Username",
            "maxlength": "40",
            "minlength": "3",
            "autocomplete": "new-username",
        })

        self.fields["email"].label = ""
        self.fields["email"].widget.attrs.update({
            "required": True,
            "name": "email",
            "id": "email",
            "type": "email",
            "class": "input-form",
            "placeholder": "Email",
            "autocomplete": "new-email",
        })
        self.fields["password1"].label = ""
        self.fields["password1"].help_text = ""
        self.fields["password1"].widget.attrs.update({
            "required": True,
            "name": "password1",
            "id": "password1",
            "type": "password",
            "placeholder": "Password",
            "class": "input-form",
            "maxlength": "40",
            "minlength": "8",
            'autocomplete': 'new-password',
        })

        self.fields["password2"].label = ""
        self.fields["password2"].help_text = ""
        self.fields["password2"].widget.attrs.update({
            "required": True,
            "name": "password2",
            "id": "password2",
            "type": "password",
            "placeholder": "Repeat password",
            "class": "input-form",
            "maxlength": "40",
            "minlength": "8",
            'autocomplete': 'new-password',
        })

        self.fields["terms_of_service"].widget.attrs.update({
            "required": True,
            "name": "terms_of_service",
            "id": "terms_of_service",
            "class": "input-form form-check-input",
            "autocomplete": "off",
        })

        self.helper.layout = Layout(
            "username",
            "email",
            "password1",
            "password2",
            Div(
                "terms_of_service", css_class="form-check d-flex justify-content-center my-4"
            ),
            Div(
                Submit("submit", "Register", css_class="btn btn-success"),
                css_class="d-flex justify-content-center my-4")
        )

class BookingForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['bike_instance', 'start_time', 'end_time', 'total_cost']
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }


    def __init__(self, *args, **kwargs):
        bike_model = kwargs.pop('bike_model', None)
        print("Bike model in form:", bike_model)
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.form_show_errors = True
        self.helper.error_text_inline = True
        self.helper.help_text_inline = False

        if bike_model:
            self.fields['bike_instance'].queryset = BikeInstance.objects.filter(bike_model=bike_model)
        else:
            self.fields['bike_instance'].queryset = BikeInstance.objects.filter(status='available')


        self.fields["bike_instance"].label = "Select Size"
        self.fields["bike_instance"].widget.attrs.update({
            "required": True,
            "class": "input-form",
            "placeholder": "Select Size",
        })

        self.fields["start_time"].label = "Start Time"
        self.fields["start_time"].widget.attrs.update({
            "required": True,
            "type": "datetime-local",
            "placeholder": "Start Time",
        })

        self.fields["end_time"].label = "End Time"
        self.fields["end_time"].widget.attrs.update({
            "required": True,
            "type": "datetime-local",
            "placeholder": "End Time",
        })
        self.helper.layout = Layout(
            'bike_instance',
            Row(
                Column('start_time', css_class=''),
                Column('end_time', css_class=''),
                css_class='row'
            ),
            Div(
                Submit("submit", "Book Now", css_class="btn btn-success"),
                css_class="d-flex justify-content-center my-4")
        )

    def clean(self):
        cleaned_data = super().clean()
        now = timezone.now()

        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')
        selected_bike = cleaned_data.get('bike_instance')

        if start_time < now - timezone.timedelta(minutes=1):
            raise forms.ValidationError("Please choose a correct date. The date cannot be in the past.")

        elif start_time and end_time and end_time <= start_time:
            raise forms.ValidationError("The end date must be after the start date.")

        if start_time and end_time and selected_bike:
            is_reserved = Reservation.objects.filter(Q(start_time__lte=end_time) & Q(end_time__gte=start_time),
                                                    bike_instance=selected_bike).exists()
            if is_reserved:
                raise forms.ValidationError("This bike is not available for the selected dates.")

        return cleaned_data