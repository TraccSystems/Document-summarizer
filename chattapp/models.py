from django.db import models
from django.contrib.auth.models import User


# Extending User Model Using a One-To-One Link
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(default='profile_images/default_profile.png', upload_to='profile_images/')
    bio = models.TextField()
    vectordb_index_name = models.CharField(max_length=255)

    def __str__(self):
        return self.user.username