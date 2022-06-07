from config import *
from TikTokApi import TikTokApi

def scrape_tiktoks():
    api = TikTokApi()
    print(api)
    something = api.trending.videos(count=10)
    print(something)
    for video in something:
        print(video)
        download(video.bytes, "test.mp4") #f"{TIKTOKPATH}/{video.id}.mp4")   
        print("Downloaded:", video.id)

def download(bytes, file_name):
    with open(file_name, 'wb') as file:
        file.write(bytes)

if "__main__" == __name__:
    print(f"Scraping Videos...")
    scrape_tiktoks()
    print(f"Scraped Videos!")
    print(f"{TIKTOKPATH}")