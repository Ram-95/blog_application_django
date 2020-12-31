from django.db import models
from django.contrib.auth.models import User
from PIL import Image

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='profile_pics', default='default.png')

    def __str__(self):
        return f'{self.user.username}\'s Profile'

    # Overriding the default save() method. To decrease the resolution of Profile Images
    def save(self):
        # saves the data of Profile class
        super().save()
        img = Image.open(self.profile_pic.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.profile_pic.path)

    
