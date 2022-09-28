import os

import environ
import requests
from ckeditor.fields import RichTextField
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from hintshare.users.models import User

env = environ.Env()


class Question(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=10000)
    # content = models.TextField(null=True, blank=True)
    content = RichTextField()
    likes = models.ManyToManyField(User, related_name="question_post")
    date_created = models.DateTimeField(default=timezone.now)
    total_like = models.IntegerField(null=True)

    class Tags(models.TextChoices):
        Math = "Ma", _("Math")
        Science = "Sc", _("Science")
        Language = "La", _("Language")
        Socials = "So", _("Socials")
        General = "Ge", _("General")

    tags = models.CharField(
        max_length=2,
        choices=Tags.choices,
        default=Tags.General,
    )

    def __str__(self):
        return f"{self.user.username} - Question"

    def get_absolute_url(self):
        return reverse("stackbase:question-detail", kwargs={"pk": self.pk})

    def total_likes(self):
        return self.likes.count()


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    question = models.ForeignKey(
        Question, related_name="comment", on_delete=models.CASCADE
    )
    title = models.CharField(max_length=1000)
    content = RichTextField()
    date_created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return "{} - {}".format(self.question.title, self.question.user)

    def get_success_url(self):
        return reverse("stackbase:question-detail", kwargs={"pk": self.pk})

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    # , reciever, sender, questionlink
    def send_simple_message():
        return requests.post(
            
            auth=(),
            data={
                "from": "",
                "to": ["dilreetraju@gmail.com"],
                "subject": "HintShare comment",
                "text": f"You have recieved a comment your post from {{sender}}. Here is a link to visit your question: {{questionlink}} ",
            },
        )
