from django import forms
from django.contrib.auth.models import User
from allauth.account.forms import LoginForm as AllauthLoginForm, SignupForm, ResetPasswordForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Div
from django.urls import reverse
from django.utils.safestring import mark_safe

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

