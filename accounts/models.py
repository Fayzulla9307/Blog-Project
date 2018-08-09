from django.db import models
from django.urls import reverse

class Post(models.Model):

    def get_absolute_url(self):
        return reverse('login', args=[str(self.id)])

# Create your models here.
