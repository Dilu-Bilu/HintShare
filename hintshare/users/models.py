from ast import BinOp
from sched import scheduler
from django.core.files.storage import default_storage as storage
from django.contrib.auth.models import AbstractUser
from django.db.models import CharField, ImageField, TextField, EmailField
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from PIL import Image

choices = [("s12", "student grade 12"), ("s11", "student grade 11"), ("t", "teacher")]


class User(AbstractUser):
    """
    Default custom user model for hintshare.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """

    #: First and last name do not cover name patterns around the globe
    name = CharField(_("Name of User"), blank=True, max_length=255)
    secondary_email = EmailField(null=True, blank=True)
    first_name = None  # type: ignore
    last_name = None  # type: ignore
    bio = TextField(
        _("A quick description of who you are."),
        blank=True,
        max_length=255,
    )
    HL = CharField(_("Your HLs"), blank=True, max_length=255)
    SL = CharField(_("Your SLs"), blank=True, max_length=255)
    Role = CharField(
        _("Role: teacher, student_11, or student_12?"), blank=True, max_length=255
    )

    Image = ImageField(default="default.jpg", upload_to="profile_pic")

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(storage.open(self.Image.name))
        img = img.convert('RGB')
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            fh = storage.open(self.Image.name, "wb")
            format = 'jpeg'  # You need to set the correct image format here
            img.save(fh, format)
            fh.close()

    def get_absolute_url(self):
        """Get url for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})
