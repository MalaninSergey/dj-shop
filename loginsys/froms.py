from django import forms
from django.contrib.auth import password_validation, authenticate
from django.contrib.auth.forms import UsernameField, UserModel
from django.contrib.auth.models import User
from django.forms import EmailField
from django.utils.text import capfirst


class RegisterForm(forms.ModelForm):
    """
       A form that creates a user, with no privileges, from the given username and
       password.
       """
    error_messages = {
        'password_mismatch': "The two password fields didn't match.",
    }
    email = forms.EmailField(
        label='Email',
        widget=forms.TextInput(attrs={'slot': "input", 'placeholder': "E-mail"}),
    )
    password1 = forms.CharField(
        label='Password',
        strip=False,
        widget=forms.PasswordInput(attrs={'slot': "input", 'placeholder': "Пароль"}),
    )
    password2 = forms.CharField(
        label="Password confirmation",
        widget=forms.PasswordInput(attrs={'slot': "input", 'placeholder': "Повторите пароль"}),
        strip=False,
        help_text="Enter the same password as before, for verification.",
    )

    class Meta:
        model = User
        fields = ("email",)
        field_classes = {'email': EmailField}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self._meta.model.USERNAME_FIELD in self.fields:
            print("text")
            self.fields[self._meta.model.USERNAME_FIELD].widget.attrs.update({'autofocus': True})

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def _post_clean(self):
        super()._post_clean()
        # Validate the password after self.instance is updated with form data
        # by super().
        password = self.cleaned_data.get('password2')
        if password:
            try:
                password_validation.validate_password(password, self.instance)
            except forms.ValidationError as error:
                self.add_error(None, error.messages)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data.get('email')
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    email = EmailField(widget=forms.TextInput(attrs={'slot': 'input', 'placeholder': "E-mail"}))
    password = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={'slot': 'input', 'placeholder': "Пароль"}),
    )

    error_messages = {
        'invalid_login':
            "Please enter a correct email and password. Note that both "
            "fields may be case-sensitive.",
        'inactive': "This account is inactive.",
    }

    def __init__(self, request=None, *args, **kwargs):
        """
        The 'request' parameter is set for custom auth use by subclasses.
        The form data comes in via the standard 'data' kwarg.
        """
        self.request = request
        self.user_cache = None
        super().__init__(*args, **kwargs)

        self.email = UserModel._meta.get_field(UserModel.EMAIL_FIELD)
        self.fields['email'].max_length = self.email.max_length or 254
        if self.fields['email'].label is None:
            self.fields['email'].label = capfirst(self.email.verbose_name)

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        print(email, password)
        if email is not None and password:
            self.user_cache = authenticate(self.request, username=email, password=password)
            if self.user_cache is None:
                print('text')
                raise self.get_invalid_login_error()
            else:
                print('text1')
                self.confirm_login_allowed(self.user_cache)
        elif email is None and password:
            raise self.get_invalid_login_error()
        return self.cleaned_data

    def confirm_login_allowed(self, user):
        """
        Controls whether the given User may log in. This is a policy setting,
        independent of end-user authentication. This default behavior is to
        allow login by active users, and reject login by inactive users.

        If the given user cannot log in, this method should raise a
        ``forms.ValidationError``.

        If the given user may log in, this method should return None.
        """
        if not user.is_active:
            raise forms.ValidationError(
                self.error_messages['inactive'],
                code='inactive',
            )

    def get_user(self):
        return self.user_cache

    def get_invalid_login_error(self):
        return forms.ValidationError(
            self.error_messages['invalid_login'],
            code='invalid_login',
            params={'email': self.email.verbose_name},
        )
