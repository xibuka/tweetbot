import tweepy
import os

# 先ほど取得した各種キーを代入する
CK="M1qtHqTD6yjvDRwh32PYuVES2" #CONSUMER_KEY
CS="2srreXQA2SlbSS8znx3XMxn4sZ6X7ReBu6gFAeaqCpWvj6mzWi"# "CONSUMER_SECRET"
AT="854237795073671169-ZPmhEDJ1SOnOmbAGEQ1veK2pORVG6P2"#"ACCESS_TOKEN"
AS="x79lLn7Hbq9hxcnDFBExFCs6yrIMKTRWmgovXMhYdP7dy"#"ACCESS_SECRET"

# Twitterオブジェクトの生成
auth = tweepy.OAuthHandler(CK, CS)
auth.set_access_token(AT, AS)

api = tweepy.API(auth)

# ツイート

res = os.system('curl inet-ip.info/ip')
print(res)
#api.update_status("Hello World!")
