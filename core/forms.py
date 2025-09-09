import datetime
from django import forms
from django.contrib.auth.models import User
from allauth.account.forms import LoginForm as AllauthLoginForm, SignupForm, ResetPasswordForm, ChangePasswordForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Div, Field, Row, Column, HTML, Button
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils import timezone
from .models import Reservation, BikeInstance, Profile
from django.db.models import Q
from django.db import transaction



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

class CrispyChangePasswordForm(ChangePasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.form_action = reverse("account_set_password")
        self.helper.form_show_errors = True
        self.helper.error_text_inline = True
        self.helper.help_text_inline = False
        self.fields["oldpassword"].label = ""
        self.fields["oldpassword"].widget.attrs.update({
            "required": True,
            "id": "id_oldpassword",
            "type": "password",
            "class": "input-form",
            "placeholder": "Current Password",
            "autocomplete": "current-password",
        })
        self.fields["password1"].label = ""
        self.fields["password1"].widget.attrs.update({
            "required": True,
            "id": "id_password1",
            "type": "password",
            "class": "input-form",
            "placeholder": "New Password",
            "autocomplete": "new-password",
        })
        self.fields["password2"].label = ""
        self.fields["password2"].widget.attrs.update({
            "required": True,
            "id": "id_password2",
            "type": "password",
            "class": "input-form",
            "placeholder": "New Password (again)",
            "autocomplete": "new-password",
        })
        self.helper.layout = Layout(
            'oldpassword',
                    'password1',
                    'password2',
            Div(
                Submit("submit", "Change password", css_class="btn btn-success"),
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
        label=mark_safe("I agree to the <a href='/terms/' class='terms-text fw-bold text-body'>Terms of Service</a>"),
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


class EditBookingForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['bike_instance', 'start_time', 'end_time', 'total_cost']
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.instance = kwargs.get('instance')
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.form_show_errors = True
        self.helper.error_text_inline = True
        self.helper.help_text_inline = False

        self.fields['bike_instance'].disabled = True
        self.fields["bike_instance"].label = ""
        self.fields['bike_instance'].widget.attrs['class'] = 'form-control no-arrow'

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
                Submit("submit", "Update Booking", css_class="btn btn-success"),
                css_class="d-flex justify-content-center my-4")
        )

    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')

        if start_time and end_time:
            bike_instance = self.instance.bike_instance

            conflicting_reservations = Reservation.objects.filter(
                bike_instance=bike_instance,
                start_time__lt=end_time,
                end_time__gt=start_time
            ).exclude(pk=self.instance.pk)

            if conflicting_reservations.exists():
                raise forms.ValidationError(
                    "These dates are already reserved for this bike. Please choose different dates.")

        return cleaned_data


class ProfileForm(forms.ModelForm):
    username = forms.CharField(max_length=100, required=True)
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)
    email = forms.CharField(max_length=100, required=True)

    class Meta:
        model = Profile
        fields = fields = ["phone_number", "profile_picture", "birth_date", "city", "street_address", "zip_code",
                           "country"]

        widgets = {
            "birth_date": forms.DateInput(attrs={"type": "date"}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.form_class = "profile_form"
        self.helper.form_show_errors = True
        self.helper.error_text_inline = True
        self.helper.help_text_inline = False
        self.fields["profile_picture"].label = False
        self.fields["profile_picture"].help_text = ""

        if self.user:
            self.fields['username'].initial = self.user.username
            self.fields['first_name'].initial = self.user.first_name
            self.fields['last_name'].initial = self.user.last_name
            self.fields['email'].initial = self.user.email

        self.helper.layout = Layout(
        Div(
            Row(
            Column(
                    HTML(
                        '''
                        <div id="photo-display-container">
                            <div class="d-flex flex-column align-items-center ">
                                {% load static %}
                                {% if form.instance.profile_picture %}
                                    <img id="profile-pic" src="{{ form.instance.profile_picture.url }}" class="img-fluid profile-picture mb-3" alt="Profile Picture">
                                {% else %}
                                    <img id="profile-pic" src="{% static 'media/profile_pics/default_profile.webp' %}" class="img-fluid profile-picture mb-3" alt="Default Profile Picture">
                                {% endif %}   
                                <button type="button" id="change-photo-btn" class="btn btn-success ">Change Photo</button>                                                          
                            </div>
                        </div>
                        '''
                    ),
                    Div(
                        Field('profile_picture'),
                        css_id="file-input-section",
                        style="display: none;"
                    ),
                    css_class='col-12 col-md-6 d-flex flex-column justify-content-center align-items-center'
                        ),
                    Column(
                            'username',
                            'first_name',
                            'last_name',
                            'email',
                            css_class='col-12 col-md-6'
                        ),
                        css_class="d-flex justify-content-center"
                    ),
                    css_class="profile-header-section"
                ),
                Div(
                HTML("<hr>"),
                    Row(
                    Column('phone_number', css_class='col-12 col-md-6'),
                        Column('birth_date', css_class='col-12 col-md-6'),
                        css_class='d-flex justify-content-start'),
                    Row(
                    Column('country', css_class='col-12 col-md-6'),
                        Column('city', css_class='col-12 col-md-6'),
                        css_class='d-flex justify-content-start'),
                    Row(
                    Column('street_address', css_class='col-12 col-md-6'),
                        Column('zip_code', css_class='col-12 col-md-6'),
                        css_class='d-flex justify-content-start'),
                        css_class="profile-form"),
                    Div(
                HTML("""
                          <a href="{% url 'account_set_password' %}" class="btn btn-success">Change Password</a>
                        """),
                Submit("submit", "Update Data", css_class="btn btn-success"),
                css_class="d-flex justify-content-center gap-4 my-4"),
        )

    @transaction.atomic
    def save(self, *args, **kwargs):
        profile = super().save(commit=False)
        profile.save()

        if self.user:
            self.user.username = self.cleaned_data['username']
            self.user.first_name = self.cleaned_data['first_name']
            self.user.last_name = self.cleaned_data['last_name']
            self.user.email = self.cleaned_data['email']
            self.user.save()

        return profile
