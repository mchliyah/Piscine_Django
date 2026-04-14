from django.db import models
from django.conf import settings


class Tip(models.Model):
    content = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    tip_date = models.DateTimeField(auto_now_add=True)
    upvoters = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="upvoted_tips", blank=True)
    downvoters = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="downvoted_tips", blank=True)

    def __str__(self):
        return f"Tip by {self.author.username} on {self.tip_date}"
