from django.db import models

class TwitterUser(models.Model):
    username = models.CharField(max_length=100)
    user_id  = models.IntegerField(primary_key=True, max_length=100)
    
    def __str__(self):
        return self.username

class UserTweet(models.Model):
    """
        Tweets from a specific user
    """

    message = models.CharField(max_length=1000)
    user = models.ForeignKey('TwitterUser', on_delete=models.RESTRICT)
    tweet_id = models.IntegerField(primary_key=True)

