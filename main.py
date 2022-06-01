import logging
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
videoDirectory = f"./{config.HASHTAG} {num_to_month[now.month]}_{str(now.day)}_{str(now.year)}"
OUTRO_VID = config.OUTPUTPATH

def setup():
    if not os.path.exists(videoDirectory): os.makedirs(videoDirectory)  # If path don't exist, make it
    if not os.path.exists(OUTRO_VID): os.makedirs(OUTRO_VID)            # For the input and output videos 
    now = datetime.datetime.now()                                       # Get now and show now
    logging.info(f"Setup run at [{now.hour}:{now.minute}:{now.second} {num_to_month[now.month]}/{now.day}/{now.year}]")

def routine():
    setup()             # Step 0: Setup
    scrape_tiktoks()    # Step 1: Scrape Videos
    makeCompilation()   # Step 2: Make Compilation
    upload_video()      # Step 3: Upload to Youtube 
    cleanup()           # Step 4: Cleanup

def attemptRoutine():
    while True:
        try:                                # When routine runs we stop
            routine()                       # If it fails, we try again in a minute
            break
        except OSError as err:              
            now = datetime.datetime.now()
            logging.error(f"Routine Failed on {now.hour}:{now.minute}:{now.second} OS error: {0}".format(err))
            time.sleep(60)

# If I use python 3.10, I can use a match case for user input on how often to run the TikTok routine

DAILY_SCHEDULED_TIME = "20:00"
schedule.every().day.at(DAILY_SCHEDULED_TIME).do(attemptRoutine)
attemptRoutine()    # Make one video right now
while True:         # and daily at the chosen time
    schedule.run_pending()  
    time.sleep(60)



