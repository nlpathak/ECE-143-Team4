from django.db import models
import datetime

class TwitterUser(models.Model):
    username = models.CharField(max_length=100, default="")
    id  = models.CharField(primary_key=True, max_length=30)
    name = models.CharField(max_length=100, default="")
    created_at = models.DateTimeField(default=datetime.datetime(1980, 1, 1, 0, 1, 1))
    description = models.CharField(max_length=100, default="")

    def __str__(self):
        return self.username
    def get_absolute_url(self):
        return f"/user/{self.username.lower()}"

class UserTweet(models.Model):
    """
        Tweets from a specific user
    """

    message = models.CharField(max_length=1000)
    username = models.ForeignKey('TwitterUser', on_delete=models.RESTRICT)
    tweet_id = models.IntegerField(primary_key=True)

