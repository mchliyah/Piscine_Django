from django.apps import apps
from django.contrib.auth.models import AbstractUser
from django.db.models import Count


class User(AbstractUser):
    @property
    def reputation(self):
        tip_model = apps.get_model("ex02", "Tip")
        aggregates = tip_model.objects.filter(author=self).aggregate(
            upvotes=Count("upvoters", distinct=True),
            downvotes=Count("downvoters", distinct=True),
        )
        upvotes = aggregates.get("upvotes") or 0
        downvotes = aggregates.get("downvotes") or 0
        return upvotes * 5 - downvotes * 2

    def can_downvote_tip(self, tip):
        return self == tip.author or self.reputation >= 15

    def can_delete_tip(self, tip):
        return self == tip.author or self.reputation >= 30
