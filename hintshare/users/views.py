from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView, RedirectView, UpdateView
from django.forms import ValidationError
User = get_user_model()


class UserDetailView(LoginRequiredMixin, DetailView):

    model = User
    slug_field = "username"
    slug_url_kwarg = "username"
    # email = object.email
    # email_str = f"https://mail.google.com/mail/?view=cm&fs=1&to=someone@example.com&su=SUBJECT&body=BODY&bcc={email}"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["now"] = "nothing"

        return context


user_detail_view = UserDetailView.as_view()


class UserUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):

    model = User
    fields = ["secondary_email","name", "bio", "Image", "HL", "SL", "Role"]
    success_message = _("Information successfully updated")

    def clean(self):
        data = self.cleaned_data["secondary_email"]
        if "@gmail.com" in data:
            print('gmail')
            return data
    
        elif "@yahoo.com" in data:
            print('yhoo')
            return data
        elif "@hotmail.com" in data:  # any check you need
           print('hot')
           return data
        else:
            print("nothing")
            raise ValidationError("Must be a surreyschools or gmail account")
        return data
    def get_success_url(self):
        assert (
            self.request.user.is_authenticated
        )  # for mypy to know that the user is authenticated
        return self.request.user.get_absolute_url()

    def get_object(self):
        return self.request.user


user_update_view = UserUpdateView.as_view()


class UserRedirectView(LoginRequiredMixin, RedirectView):

    permanent = False

    def get_redirect_url(self):
        return reverse("users:detail", kwargs={"username": self.request.user.username})


user_redirect_view = UserRedirectView.as_view()
