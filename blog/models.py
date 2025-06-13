import cloudinary.uploader
from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField

STATUS = (
    (0, "Draft"),
    (1, "Publish")
)


class Post(models.Model):
    title = models.CharField(max_length=300)
    slug = models.SlugField(max_length=300, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    header_image = CloudinaryField('image', blank=False, null=False)
    content = models.TextField()
    status = models.IntegerField(choices=STATUS, default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def delete(self, *args, **kwargs):
        public_id = getattr(self.header_image, "public_id", None)
        if public_id:
            cloudinary.uploader.destroy(public_id)
        super().delete(*args, **kwargs)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return self.title
