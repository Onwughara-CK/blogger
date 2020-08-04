from django.db import models
from django.contrib.auth.models import User
from PIL import Image


class Profile(models.Model):
    """
    use to create users profile
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.png', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username}'

    def save(self):
        super().save()

        image_path = self.image.path
        image = Image.open(image_path)
        MAX_SIZE = (125, 125)
        image.thumbnail(MAX_SIZE)
        image.save()
