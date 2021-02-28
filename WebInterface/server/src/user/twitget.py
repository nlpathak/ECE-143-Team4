import os
import requests
import json
import logging.config


class TwitGet():
    logger = logging.getLogger('TWITGET')

    def __init__(self):
        self.bearer = os.environ['BEARER_TOKEN']
        self.headers = {'Authorization':f"Bearer {self.bearer}"}
        self.tweet_params = {"tweet.fields": "created_at", "max_results":100}
        self.user_fields = "user.fields=description,created_at,profile_image_url,public_metrics,url,verified"
 
    def __repr__(self):
        return "TwitGet()"

    def create_url(self, user_x):
        '''
        Gets a url based off of user_x. User_x should either be
        username or user id.
        :param user_x: User-id or str of username
        '''
        assert len(user_x) > 0
        assert isinstance(user_x, str)
        url = ''
        try:
            if user_x.isdigit():
                user_id = user_x
                url = f"https://api.twitter.com/2/users/{user_id}/tweets"
            else:
                usernames = "usernames=" + user_x
                url = f"https://api.twitter.com/2/users/by?{usernames}&{self.user_fields}"
            return url
        except AssertionError:
            self.logger.error('Error creating url in twitget')

    def connect_to_endpoint(self, UserNms, params=None):
        url = self.create_url(UserNms)
        if params:
            response = requests.request("GET", url, headers=self.headers, params=params)
        else:
            response = requests.request("GET", url, headers=self.headers)

        self.logger.debug('get_users_with_bearer_token ... \tResponse status code: Success!' 
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

    def get_user(self, user_x):
        '''
        '''
        assert isinstance(user_x,str)
        assert len(user_x) > 0
        url = self.create_url(user_x)
        json_response = self.connect_to_endpoint(user_x)
        return json_response


    def get_tweets(self, user_id, tweetCount):
        url = self.create_url(user_id)
        json_response = self.connect_to_endpoint(user_id, params=self.tweet_params)
        tweets = []
        if json_response and 'data' in json_response:

            tweets = json_response['data']

            #Get next pagination token, if possible
            try:
                self.tweet_params = {**self.tweet_params, 'pagination_token':json_response['meta']['next_token']}
            except:
                self.tweet_params = {**self.tweet_params, 'pagination_token':None}
            pagination_count = 1 #controls incremental amounts of tweets by max_count of pagination
            self.logger.debug('Pagination progress: ', pagination_count, '/', int(tweetCount / 100))

            while self.tweet_params['pagination_token'] and pagination_count < tweetCount/100:
                pagination_count += 1
                json_response = self.connect_to_endpoint(url, self.tweet_params)
                self.logger.debug('Pagination progress: ', pagination_count, '/', int(tweetCount/100))
                try:
                    self.tweet_params['pagination_token'] = json_response['meta']['next_token']
                except:
                    self.tweet_params['pagination_token'] = False
                tweets.append(json_response['data'])

            if pagination_count != int(tweetCount/100):
                self.logger.debug('Reached end of content from user before specified request amount.')
            return tweets
        else:
            return []
