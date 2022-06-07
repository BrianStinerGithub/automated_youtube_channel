from config import *
from time import sleep
from TikTokApi import TikTokApi
import logging
import string
import random
import urllib

def scrape_tiktoks():
    with TikTokApi as api:
        for tiktok in api.search.hashtags(HASHTAG, count=100):
            if tiktok.video_url:
                download(tiktok.video_url, f"{TIKTOKPATH}/{tiktok.id}.mp4")
                print(f"Downloaded {tiktok.id}")

def scrape_tiktoks_old():
    rid = ''.join(random.choice(string.digits) for _ in range(19))                                                                                          # Make a random 19 digit number for API
    api = TikTokApi.get_instance(proxy="213.137.240.243:81", custom_verifyFP=TIKTOKCOOKIE, custom_device_id=rid)                                            # Get TikTok API a proxy, cookie, and id
    tiktoks = api.by_hashtag(HASHTAG, 100)                                                                                                                  # Get 100 TikToks by searching with hashtag
    minute, second, microsecond = str(NOW.minute), str(NOW.second), str(NOW.microsecond)                                                                    # Get time
    for tiktok in tiktoks:                                                                                                                                  #
        downloadURL = tiktok['video']['downloadAddr']                                                                                                       # Download the TikToks to folder. 
        title = f"{tiktok['author']['nickname']}{tiktok['desc'][:15]} {minute}:{second}:{microsecond}".translate(str.maketrans('', '', string.punctuation)) # Each TikTok has a title with the 
        download(downloadURL, f"{TIKTOKPATH}/{title}.mp4")                                                                                                  # TikToker's name, description, time minus punctuation.

def download(url, file_name):
    with open(file_name, 'wb') as f:
        response = urllib.request.urlopen(url)
        f.write(response.read())

if "__main__" == __name__:
    logging.info("Scraping Videos...")
    scrape_tiktoks()
    logging.info("Scraped Videos!")