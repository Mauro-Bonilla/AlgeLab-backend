from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    github_username = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.user.username

    @property
    def avatar_url(self):
        if self.github_username:
            return f"https://github.com/{self.github_username}.png"
        return None