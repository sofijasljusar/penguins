from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.contrib import messages
from .forms import ContactForm
# Create your views here.

import requests

BLOG_POSTS = requests.get('https://api.npoint.io/ce3b8ba44b768e2a827e').json()
class HomeView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["post_list"] = BLOG_POSTS
        return context


class AboutView(TemplateView):
    template_name = "about.html"


class ContactView(FormView):
    template_name = "contact.html"
    form_class = ContactForm
    success_url = reverse_lazy("contact")

    def form_valid(self, form):
        messages.success(self.request, "Повідомлення було успішно надіслано!")
        return super().form_valid(form)


class PostDetail(TemplateView):
    template_name = "post_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = kwargs.get('slug')
        post = next((p for p in BLOG_POSTS if p["slug"] == slug), None)
        if post:
            context["post"] = post
        else:
            context["post"] = {"title": "Not Found", "content": "This post does not exist."}

        return context
