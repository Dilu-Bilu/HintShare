from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.core.mail import send_mail
from hintshare.users.forms import UserAdminChangeForm, UserAdminCreationForm

User = get_user_model()


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):

    form = UserAdminChangeForm
    add_form = UserAdminCreationForm
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("name", "email")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    list_display = ["username", "name", "secondary_email", "is_superuser"]

    search_fields = ["name", "secondary_email"]
    actions = ['make_published']

    @admin.action(description='Send promotional emails')
    def make_published(self, request, queryset):
        print("Yo")
        for obj in queryset:
            sender = "dilreetraju@hintshare.ca"
            reciever = str(obj.email)
        
            subject = "Hintshare Checking Reminder"
            message = f"There are new questions available on HintShare; log on to check them out."
            send_mail(subject, message, sender,
            [reciever], html_message=f"<html>{message} <a href = 'https://hintshare.ca/questions/'>See Questions!</a></html>")
            print(subject, message, sender)
            try:
                reciever2 = str(obj.secondary_email)
                send_mail(subject, message, sender,
                [reciever2], html_message=f"<html>{message} <a href = 'https://hintshare.ca/questions/'>See Question!</a></html>")
            except:
                pass
       
    
