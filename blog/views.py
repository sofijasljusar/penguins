import os
import smtplib
import cloudinary.uploader

from django.views.generic import TemplateView, DetailView, ListView
from django.views.generic.edit import FormView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.utils.http import url_has_allowed_host_and_scheme
from django.urls import reverse_lazy
from django.contrib import messages
from .forms import ContactForm, RegisterForm, LoginForm, PostForm
from dotenv import load_dotenv
from .models import Post
from django.urls import reverse

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
        next_page = self.request.GET.get("next")
        if next_page and url_has_allowed_host_and_scheme(next_page, allowed_hosts={self.request.get_host()}):
            return next_page
        return reverse_lazy("home")


class UserLogoutView(LogoutView):
    next_page = reverse_lazy("home")


class CreatePostView(LoginRequiredMixin, UserPassesTestMixin, FormView):
    template_name = "create_post.html"
    form_class = PostForm
    success_url = reverse_lazy("home")

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_superuser

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = self.request.user
        image_file = self.request.FILES["header_image"]
        upload_result = cloudinary.uploader.upload(
            image_file,
            folder="header_images/",
            use_filename=True,
            unique_filename=True
        )
        post.header_image_url = upload_result["secure_url"]
        post.save()

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["heading"] = "Створити пост"
        return context


class EditPostView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = "create_post.html"

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_superuser

    def get_success_url(self):
        return reverse("post_detail", kwargs={"slug": self.object.slug})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["heading"] = "Редагувати пост"
        return context


class DeletePostView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = "confirm_delete_post.html"
    success_url = reverse_lazy("home")

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_superuser
