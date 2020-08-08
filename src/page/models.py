from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify


class Post(models.Model):
    """
    Model that represents post data
    """

    title = models.CharField(max_length=50)
    content = models.TextField('content')
    date_posted = models.DateTimeField('time published', default=timezone.now)
    author = models.ForeignKey(
        User, related_name='posts', on_delete=models.CASCADE)
    slug = models.SlugField(max_length=75)

    def get_absolute_url(self):
        return reverse('page:detail', args=[self.pk, self.slug])

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.title} || {self.get_absolute_url()}'
