import os
import requests
import json
import logging.config


class TwitGet():
    def __init__(self):
        self.bearer = os.environ['BEARER_TOKEN']
        self.headers = {'Authorization':f"Bearer {self.bearer}"}
 
    def __repr__(self):
        return "TwitGet()"

    def create_url(self, UserNms):
        usernames = "usernames=" + UserNms
        user_fields = "user.fields=description,created_at"
        url = f"https://api.twitter.com/2/users/by?{usernames}&{user_fields}"
        return url

    def connect_to_endpoint(self, UserNms):
        url = self.create_url(UserNms)
        response = requests.request("GET", url, headers=self.headers)
        print('get_users_with_bearer_token ... \tResponse status code: Success!' 
            if response.status_code == 200 
            else 'get_users_with_bearer_token ... \tResponse status code: ' + 
            str(response.status_code))
        if response.status_code != 200:
            raise Exception(
                "Request returned an error: {} {}".format(
                response.status_code, response.text
                )
            )
        return response.json()

