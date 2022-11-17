from django.urls import path, include
from django.views.generic import TemplateView
from django.contrib.sitemaps.views import sitemap
from .sitemaps import StaticViewSitemap
from . import views

sitemaps = {
    'static': StaticViewSitemap,
}

from . import views

app_name = "stackbase"

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    # CRUD Function
    path("questions/", views.QuestionListView.as_view(), name="question-lists"),
    path("questions/new/", views.QuestionCreateView.as_view(), name="question-create"),
    path(
        "questions/<int:pk>/",
        views.QuestionDetailView.as_view(),
        name="question-detail",
    ),
    path(
        "questions/<int:pk>/update/",
        views.QuestionUpdateView.as_view(),
        name="question-update",
    ),
    path(
        "questions/<int:pk>/delete/",
        views.QuestionDeleteView.as_view(),
        name="question-delete",
    ),
    path(
        "questions/<int:pk>/comment/",
        views.AddCommentView.as_view(),
        name="question-comment",
    ),
    path("like/<int:pk>", views.like_view, name="like_post"),
    path("like/<int:pk>/<int:id>", views.comment_like_view, name="like_comment"),
    path('hitcount/', include(('hitcount.urls', 'hitcount'), namespace='hitcount')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps},
        name='django.contrib.sitemaps.views.sitemap')
]
