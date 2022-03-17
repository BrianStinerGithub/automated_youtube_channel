from scrape_tiktoks import scrape_tiktoks
from make_compilation import makeCompilation
from upload_video import upload_video
from cleanup import cleanup
import schedule
import time
import datetime
import os
from googleapiclient.discovery import build
import config

num_to_month = {
    1: "Jan",  2: "Feb",  3: "Mar",
    4: "Apr",  5: "May",  6: "June",
    7: "July", 8: "Aug",  9: "Sept",
    10: "Oct", 11: "Nov", 12: "Dec"
}
now = datetime.datetime.now()
videoDirectory = f"./{config.HASHTAG}_" + num_to_month[now.month].upper() + "_" + str(now.year) + "_V" + str(now.day) + "/"
outputFile = "./" + num_to_month[now.month].upper() + "_" + str(now.year) + "_v" + str(now.day) + ".mp4"

INTRO_VID = config.INTROPATH
OUTRO_VID = config.OUTPUTPATH
TOTAL_VID_LENGTH = config.VIDEO_LENGTH
MAX_CLIP_LENGTH = config.MAX_CLIP_LENGTH
MIN_CLIP_LENGTH = config.MIN_CLIP_LENGTH
DAILY_SCHEDULED_TIME = "20:00"

def setup():
    if not os.path.exists(videoDirectory):  os.makedirs(videoDirectory)
    if not os.path.exists(OUTRO_VID):       os.makedirs(OUTRO_VID)
    now = datetime.datetime.now()
    print(f"{now.month}/{now.day}/{now.year} {now.hour}:{now.minute}:{now.second}")

def routine():
    # Step 0: Setup
    setup()
    # Step 1: Scrape Videos
    scrape_tiktoks()
    # Step 2: Make Compilation
    makeCompilation()
    # Step 3: Upload to Youtube
    upload_video()
    # Step 4: Cleanup
    cleanup()

def attemptRoutine():
    while(1):
        try:
            routine()
            break
        except OSError as err:
            now = datetime.datetime.now()
            print(f"Routine Failed on {now.hour}:{now.minute}:{now.second} OS error: {0}".format(err))
            time.sleep(60)


schedule.every().day.at(DAILY_SCHEDULED_TIME).do(attemptRoutine)
attemptRoutine()
while True:
    schedule.run_pending()  
    time.sleep(60)



