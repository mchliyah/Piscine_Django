from django.db import models

class Article(models.Model):
    title = models.CharField(max_length=64, null=False)
    content = models.TextField(null=False)
    author = models.ForeignKey('auth.User', null=False, on_delete=models.CASCADE)
    synopsis = models.CharField(max_length=312, null=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class  UserFavouriteArticle(models.Model):
    user = models.ForeignKey('auth.User', null=False, on_delete=models.CASCADE)
    article = models.ForeignKey(Article,null=False, on_delete=models.CASCADE)

    def __str__(self):
        return self.article.title



# subject:
# ◦ title: Article’s title. Character chain 64 max size. Non null.
# ◦ author: Article’s author. References a record of the User model. Non null.
# ◦ created: Creation’s complete date and time. Must be automatically filled
# when created. Non null.
# ◦ synopsis: Article’s abstract. Character chain. Max size 312. Non null.
# ◦ content: The article. It’s a text type. Non null.
# The __str()__ method must be ’overrode’ to send ’title’


# UserFavouriteArticle: User’s favorite articles. Must feature the following fields:
# ◦ user: References a record of the User model. Non null.
# ◦ article: References a record of the Article model. Non null.
# The __str()__ method must be overridden to send ’title’ included in the Article
# model.
