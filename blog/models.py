from django.db import models
from django.utils import timezone

from django.urls import reverse
from django.shortcuts import redirect
# Create your models here.

#Post Model
class Post(models.Model):
    author = models.ForeignKey('auth.User',on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now())
    published_date = models.DateTimeField(blank=True, null=True)

    def get_absolute_url(self):
        return reverse('blog:post_list')

    def publish(self):
        self.published_date=timezone.now()
        self.save()

    def __str__(self):
        return self.title

    def approve_comment(self):
        return self.comments.filter(approved_comment=True)

#Comment Model
class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments',on_delete=models.CASCADE)
    author = models.CharField(max_length=100)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now())
    approved_comment = models.BooleanField(default=False)

    def get_absolute_url(self):
        reverse('blog:post_list')

    def approve(self):
        self.approved_comment=True
        self.save()

    def __str__(self):
        return self.text
