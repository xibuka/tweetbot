import tweepy
import logging
import time
import subprocess
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

myip = subprocess.check_output("curl inet-ip.info/ip", 
        shell=True).decode('ascii').replace(".", "|")

class tweetbot:
    def __init__(self):
        self._consumer_key    = os.getenv("CONSUMER_KEY")
        self._consumer_secret = os.getenv("CONSUMER_SECRET")
        self._access_token    = os.getenv("ACCESS_TOKEN")
        self._access_secret   = os.getenv("ACCESS_TOKEN_SECRET")

        try:
            auth = tweepy.OAuthHandler(self._consumer_key,
                                       self._consumer_secret)
            auth.set_access_token(self._access_token, self._access_secret)

            #self.client = tweepy.API(auth)
            self.client = tweepy.API(auth, wait_on_rate_limit=True, 
                    wait_on_rate_limit_notify=True)
            if not self.client.verify_credentials():
                raise tweepy.TweepError
        except tweepy.TweepError as e:
            logger.error("Error creating API", exc_info=True)
        else:
            logger.info('Connected as @{}'.format(self.client.me().screen_name))
            self.client_id  = self.client.me().id
            self.start_time = self.get_last_mentions()


    def get_last_mentions(self):
        return self.client.mentions_timeline(count=1)[0].created_at

    def check_mentions(self, keywords):
        logger.info("Retrieving mentions")
        for tweet in tweepy.Cursor(self.client.mentions_timeline).items():
            if tweet.created_at <= self.start_time:
                continue
            if any(keyword in tweet.text.lower() for keyword in keywords):
                logger.info(f"report IP address to {tweet.user.screen_name}")
    
                self.client.update_status(f"[{self.start_time}] Hi @{tweet.user.screen_name}, check 11|{myip}|12")
    
        self.start_time = self.get_last_mentions()

def main():
    myipbot = tweetbot()
    while True:
        myipbot.check_mentions(["ip"])
        logger.info("Waiting...")
        time.sleep(60)

if __name__ == "__main__":
    main()
