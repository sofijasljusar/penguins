import os
import smtplib

from django.shortcuts import render
from django.views.generic import TemplateView, DetailView, ListView
from django.views.generic.edit import FormView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from .forms import ContactForm, RegisterForm, LoginForm
from dotenv import load_dotenv
from .models import Post

load_dotenv()
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


class UserRegisterView(FormView):
    template_name = "register.html"
    form_class = RegisterForm
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)


class UserLoginView(LoginView):
    template_name = "login.html"
    form_class = LoginForm

    def get_success_url(self):
        return reverse_lazy("home")


class UserLogoutView(LogoutView):
    next_page = reverse_lazy("home")