import requests
import os
import json



# To set your environment variables in your terminal run the following line:
# export 'BEARER_TOKEN'='<your_bearer_token>'


def auth():
    return os.environ.get("BEARER_TOKEN")


def create_url(user_id):
    # Replace with user ID below
    #user_id = 2244994945
    return "https://api.twitter.com/2/users/{}/tweets".format(user_id)


def get_params():
    # Tweet fields are adjustable.
    # Options include:
    # attachments, author_id, context_annotations,
    # conversation_id, created_at, entities, geo, id,
    # in_reply_to_user_id, lang, non_public_metrics, organic_metrics,
    # possibly_sensitive, promoted_metrics, public_metrics, referenced_tweets,
    # source, text, and withheld
    return {"tweet.fields": "created_at", "max_results":100}


def create_headers(bearer_token):
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    return headers


def connect_to_endpoint(url, headers, params):
    response = requests.request("GET", url, headers=headers, params=params)
    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )
    return response.json()


def main(user_id, tweetCount):
    bearer_token = auth()
    url = create_url(user_id)
    headers = create_headers(bearer_token)
    params = get_params()
    json_response = connect_to_endpoint(url, headers, params)

    tweetList = []
    tweetDates = []
    for tweetIdx in range(len(json_response['data'])):
        tweetList.append(json_response['data'][tweetIdx]['text'])
        tweetDates.append(json_response['data'][tweetIdx]['created_at'])
    #Get next pagination token, if possible
    try:
        params = {**params, 'pagination_token':json_response['meta']['next_token']}
    except:
        params = {**params, 'pagination_token':None}
    pagination_count = 1 #controls incremental amounts of tweets by max_count of pagination
    print('Pagination progress: ', pagination_count, '/', int(tweetCount / 100))
    while params['pagination_token'] and pagination_count < tweetCount/100:
        pagination_count += 1
        json_response = connect_to_endpoint(url, headers, params)
        print('Pagination progress: ', pagination_count, '/', int(tweetCount/100))
        try:
            params['pagination_token'] = json_response['meta']['next_token']
        except:
            params['pagination_token'] = False
        for tweetIdx in range(len(json_response['data'])):
            tweetList.append(json_response['data'][tweetIdx]['text'])
            tweetDates.append(json_response['data'][tweetIdx]['created_at'])
    if pagination_count != int(tweetCount/100):
        print('Reached end of content from user before specified request amount.')

    return tweetList, tweetDates


if __name__ == "__main__":
    main()
