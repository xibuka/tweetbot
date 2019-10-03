import tweepy
import logging
from config import create_api
import time
import os
import subprocess

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

def check_mentions(api, keywords, since_id):
    logger.info("Retrieving mentions")
    new_since_id = since_id
    for tweet in tweepy.Cursor(api.mentions_timeline, since_id=since_id).items():
        new_since_id = max(tweet.id, new_since_id)
        if tweet.in_reply_to_status_id is not None:
            continue
        if any(keyword in tweet.text.lower() for keyword in keywords):
            logger.info(f"report IP address to {tweet.user.screen_name}")

            if not tweet.user.following and not tweet.user.screen_name == 'tweetwalkershi':
                tweet.user.follow()

            myip = subprocess.check_output("curl inet-ip.info/ip", shell=True);
            myip = myip.decode('ascii');
            myip = myip.replace(".", "|")
                      
            text=f"@{tweet.user.screen_name} Hi, check 121|{myip}|121"

            api.update_status(
                status=text,
                in_reply_to_status_id=tweet.id,
            )
    return new_since_id

def main():
    api = create_api()
    since_id = 1
    while True:
        since_id = check_mentions(api, ["ip"], since_id)
        logger.info("Waiting...")
        time.sleep(60)

if __name__ == "__main__":
    main()
