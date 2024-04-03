from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    body = models.TextField()
    slug = models.SlugField()
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.body
