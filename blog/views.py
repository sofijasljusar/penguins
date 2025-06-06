from django.shortcuts import render
from django.views import generic
# Create your views here.

import requests


class HomeView(generic.TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["post_list"] = requests.get('https://api.npoint.io/ce3b8ba44b768e2a827e').json()
        return context


class AboutView(generic.TemplateView):
    template_name = "about.html"


class ContactView(generic.TemplateView):
    template_name = "contact.html"
