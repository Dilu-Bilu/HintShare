import os

import requests
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db import models
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from hintshare.users.models import User

from .forms import CommentForm
from .models import Comment, Question


def home(request):
    questions = Question.objects.all().count()
    users = User.objects.all().count()
    print(questions, users)

    context = {
        "questions": questions,
        "users": users,
    }

    return render(request, "pages/home.html", context)


def about(request):
    return render(request, "about.html")


# CRUD Function
def like_view(request, pk):
    post = get_object_or_404(Question, id=request.POST.get("question_id"))
    liked = False
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        liked = False
        post.total_like = post.total_likes()
    else:
        post.likes.add(request.user)
        liked = True
    return HttpResponseRedirect(reverse("stackbase:question-detail", args=[str(pk)]))


class QuestionListView(ListView):
    model = Question
    context_object_name = "questions"
    ordering = ["-date_created"]
    paginate_by = 8

    # def get_queryset(self):
    #     filter_val = self.request.GET.get('filter', 'give-default-value')
    #     order = self.request.GET.get('orderby', 'give-default-value')
    #     new_context = Question.objects.filter(
    #         title=filter_val,
    #     ).order_by(order)
    #     return new_context

    # def get_context_data(self, **kwargs):
    #     context = super(QuestionListView, self).get_context_data(**kwargs)
    #     context['filter'] = self.request.GET.get('filter', 'give-default-value')
    #     context['orderby'] = self.request.GET.get('orderby', 'give-default-value')
    #     return context

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search_input = self.request.GET.get("search-area") or ""
        if search_input:
            # Make sure to come back here to fix the search
            context["questions"] = Question.objects.all().filter(
                title__icontains=search_input
            )
            context["search_input"] = search_input
        return context


class QuestionDetailView(DetailView):
    model = Question

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data()
        something = get_object_or_404(Question, id=self.kwargs["pk"])
        total_likes = something.total_likes()

        liked = False
        if something.likes.filter(id=self.request.user.id).exists():
            liked = True

        context["total_likes"] = total_likes
        context["liked"] = liked
        return context


class QuestionCreateView(LoginRequiredMixin, CreateView):
    model = Question
    fields = ["title", "content", "tags"]
    context_object_name = "question"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class QuestionUpdateView(UserPassesTestMixin, LoginRequiredMixin, UpdateView):
    model = Question
    fields = ["title", "content"]

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def test_func(self):
        questions = self.get_object()
        if self.request.user == questions.user:
            return True
        return False


class QuestionDeleteView(UserPassesTestMixin, LoginRequiredMixin, DeleteView):
    model = Question
    context_object_name = "question"
    success_url = "/"

    def test_func(self):
        questions = self.get_object()
        if self.request.user == questions.user:
            return True
        return False


class CommentDetailView(CreateView):
    model = Comment
    form_class = CommentForm
    template_name = "stackbase/question-detail.html"

    def form_valid(self, form):
        form.instance.question_id = self.kwargs["pk"]
        return super().form_valid(form)

    success_url = reverse_lazy("stackbase:question-detail")


class AddCommentView(CreateView):
    model = Comment
    form_class = CommentForm

    template_name = "stackbase/question-answer.html"

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.question_id = self.kwargs["pk"]
        # sender = form.instance.user.get_email_field_name
        sender = "someone@gmail.com"
        print(sender)
        reciever = "dilreetraju@gmail.com"
        questionlink = "http://127.0.0.1:8000/"
        form.instance.send_simple_message()
        return super().form_valid(form)

    success_url = reverse_lazy("stackbase:question-lists")
