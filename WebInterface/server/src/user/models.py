from django.db import models
import datetime

class TwitterUser(models.Model):
    username = models.CharField(max_length=100, default="")
    id  = models.CharField(primary_key=True, max_length=30)
    name = models.CharField(max_length=100, default="")
    created_at = models.DateTimeField(default=datetime.datetime(1980, 1, 1, 0, 1, 1))
    description = models.CharField(max_length=200, default="")

    def __str__(self):
        return self.username
    def get_absolute_url(self):
        return f"/user/{self.username.lower()}"

class UserTweet(models.Model):
    """
        Tweets from a specific user
    """

    text = models.CharField(max_length=500)
    user = models.ForeignKey('TwitterUser', on_delete=models.RESTRICT)
    id = models.CharField(primary_key=True,max_length=50)
    created_at = models.DateTimeField(default=datetime.datetime(1980, 1, 1, 0, 1, 1))
    

