import tweepy
import logging
from config import create_api
import time
import subprocess

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

def get_localhost_public_ip():
    return subprocess.check_output("curl inet-ip.info/ip", shell=True).decode('ascii').replace(".", "|")

def check_mentions(api, keywords, start_time):
    logger.info("Retrieving mentions")
    for tweet in tweepy.Cursor(api.mentions_timeline).items():
        if tweet.created_at <= start_time:
            continue
        if any(keyword in tweet.text.lower() for keyword in keywords):
            logger.info(f"report IP address to {tweet.user.screen_name}")

            myip=get_localhost_public_ip()

            api.update_status(f"[{start_time}] Hi @{tweet.user.screen_name}, check 121|{myip}|121")

    return get_last_mentions(api)

def get_last_mentions(api):
    last_mention=api.mentions_timeline(cound=1)[0]
    return last_mention.created_at

def main():
    api = create_api()
    start_time = get_last_mentions(api)
    while True:
        start_time = check_mentions(api, ["ip"], start_time)
        logger.info("Waiting...")
        time.sleep(60)

if __name__ == "__main__":
    main()
