from django.contrib import admin
from user.models import TwitterUser, UserTweet
# Register your models here.

admin.site.register(TwitterUser)
admin.site.register(UserTweet)
