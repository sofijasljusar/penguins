from django.shortcuts import render
from django.views import generic
# Create your views here.

import requests

BLOG_POSTS = requests.get('https://api.npoint.io/ce3b8ba44b768e2a827e').json()
class HomeView(generic.TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["post_list"] = BLOG_POSTS
        return context


class AboutView(generic.TemplateView):
    template_name = "about.html"


class ContactView(generic.TemplateView):
    template_name = "contact.html"


class PostDetail(generic.TemplateView):
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
