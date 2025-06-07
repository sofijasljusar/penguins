import os
import smtplib

from django.shortcuts import render
from django.views.generic import TemplateView, DetailView, ListView
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.contrib import messages
from .forms import ContactForm
from dotenv import load_dotenv
# Create your views here.
import requests
from .models import Post

load_dotenv()
BLOG_POSTS = requests.get('https://api.npoint.io/ce3b8ba44b768e2a827e').json()
EMAIL = os.environ["EMAIL"]
PASSWORD = os.environ["PASSWORD"]


class HomeView(ListView):
    queryset = Post.objects.filter(status=1)
    template_name = "index.html"
    context_object_name = 'post_list'
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context["post_list"] = BLOG_POSTS
    #     return context


class AboutView(TemplateView):
    template_name = "about.html"


class ContactView(FormView):
    template_name = "contact.html"
    form_class = ContactForm
    success_url = reverse_lazy("contact")

    def form_valid(self, form):
        name = form.cleaned_data["name"]
        email = form.cleaned_data["email"]
        phone = form.cleaned_data["phone"]
        message = form.cleaned_data["message"]
        with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
            connection.starttls()
            connection.login(user=EMAIL, password=PASSWORD)

            connection.sendmail(from_addr=email,
                                to_addrs=EMAIL,
                                msg = f"From: {name}"
                                      f"\nTo: {EMAIL}"
                                      f"\nSubject: Запитання про пінгвінів :)"
                                      f"\n\nІм'я: {name}"
                                      f"\nПошта: {email}"
                                      f"\nТелефон: {phone}"
                                      f"\nПитання: {message}".encode("UTF-8"))

        messages.success(self.request, "Повідомлення було успішно надіслано!")
        return super().form_valid(form)


class PostDetail(DetailView):
    model = Post
    template_name = "post_detail.html"
    context_object_name = "post"
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     slug = kwargs.get('slug')
    #     post = next((p for p in BLOG_POSTS if p["slug"] == slug), None)
    #     if post:
    #         context["post"] = post
    #     else:
    #         context["post"] = {"title": "Not Found", "content": "This post does not exist."}
    #
    #     return context
