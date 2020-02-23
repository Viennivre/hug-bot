import time
import urllib.request
import os
from os import environ
from datetime import datetime
import giphy_client
import tweepy

twitter_api_key = environ['twitter_api_key']
twitter_api_secret = environ['twitter_api_secret']
twitter_access_token = environ['twitter_access_token']
twitter_access_secret = environ['twitter_access_secret']
auth = tweepy.OAuthHandler(twitter_api_key, twitter_api_secret)
auth.set_access_token(twitter_access_token, twitter_access_secret)
api = tweepy.API(auth)
hug_filename = "hug.gif"

def download_random_gif():
    giphy_api = giphy_client.DefaultApi()
    giphy_api_key = environ['giphy_api_key']
    tag = 'hug'
    fmt = 'json'
    api_response = giphy_api.gifs_random_get(giphy_api_key, tag=tag, fmt=fmt)
    
    urllib.request.urlretrieve(api_response.data.image_url, hug_filename)

def check_mentions():
    since_id = environ['since_id']
    for tweet in tweepy.Cursor(api.mentions_timeline,
        since_id=since_id).items():
        new_since_id = max(tweet.id, int(since_id))
        print('tweeting to tweet {}'.format(tweet.id))
        tweet_gif(tweet.author.screen_name, tweet.id)
        environ['since_id'] = str(new_since_id)

def tweet_gif(reply_to_user, reply_to_id):
    download_random_gif()
    # Twitter has a max upload size of 15MB
    while os.path.getsize(hug_filename) > 15000000:
        download_random_gif()

    gif_upload = api.media_upload(hug_filename)
    api.update_status(
        status="Here! Have a hug! @{}".format(reply_to_user),
        media_ids=[gif_upload.media_id],
        in_reply_to_status_id=reply_to_id
    )
    os.remove(hug_filename)

def main():
    while True:
        print("Checking mentions %s" % datetime.now())
        check_mentions()
        time.sleep(10)

if __name__ == "__main__":
    main()