import sys
sys.path.append("..") 
from django.urls import path, include
from django.views.generic import TemplateView
from django.contrib.sitemaps.views import sitemap
from hintshare.sitemaps import StaticViewSitemap, ArticleSitemap
from . import views
from django.http import HttpResponse

app_name = "stackbase"

sitemaps = {
    'static': StaticViewSitemap,
    'questions':ArticleSitemap,
}

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
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path("robots.txt",TemplateView.as_view(template_name="robots.txt", content_type="text/plain")),
    (r'^robots.txt', lambda r: HttpResponse("User-agent: *\nDisallow: /*", mimetype="text/plain")),
]
