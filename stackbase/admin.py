from django.contrib import admin

from .models import Comment, Question

# Register your models here.
admin.site.register(Question)
admin.site.register(Comment)
