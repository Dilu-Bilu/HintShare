from allauth.account.forms import SignupForm
from allauth.socialaccount.forms import SignupForm as SocialSignupForm
from django import forms
from django.contrib.auth import forms as admin_forms
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from allauth.account.utils import has_verified_email, send_email_confirmation
User = get_user_model()


class UserAdminChangeForm(admin_forms.UserChangeForm):
    class Meta(admin_forms.UserChangeForm.Meta):
        model = User


class UserAdminCreationForm(admin_forms.UserCreationForm):
    """
    Form for User Creation in the Admin Area.
    To change user signup, see UserSignupForm and UserSocialSignupForm.
    """

    class Meta(admin_forms.UserCreationForm.Meta):
        model = User

        error_messages = {
            "username": {"unique": _("This username has already been taken.")},
            "email": {"unique": _("This email has already been taken.")},
        }


class UserSignupForm(SignupForm):
    """
    Form that will be rendered on a user sign up section/screen.
    Default fields will be added automatically.
    Check UserSocialSignupForm for accounts created from social.
    """

    fields = [
        "bio",
        "Image",
    ]

    widgets = {
        "Image": forms.FileInput(attrs={"class": "input-image-control"}),
    }

    def clean_email(self):
        data = self.cleaned_data["email"]

        if "@surreyschools.ca" not in data:  # any check you need
            # if "@gmail.com" in data:
            #     return data
            raise forms.ValidationError("Must be a surreyschools account")
        # elif "@gmail.com" not in data:  # any check you need
        #     raise forms.ValidationError("Must be a Gmail account")
       
        return data

    class Meta:
        model = User
        exclude = ("user",)


class UserSocialSignupForm(SocialSignupForm):
    """
    Renders the form when user has signed up using social accounts.
    Default fields will be added automatically.
    See UserSignupForm otherwise.
    """
