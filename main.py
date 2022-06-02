import logging
from scrape_tiktoks import scrape_tiktoks
from make_compilation import makeCompilation
from upload_video import upload_video
from cleanup import cleanup
import schedule
import time
import os
from googleapiclient.discovery import build
import config


hour, minute, second = str(config.NOW.hour), str(config.NOW.minute), str(config.NOW.second)
month, day, year = config.MONTH, config.NOW.day, config.NOW.year
hashtag = config.HASHTAG
OUTRO_VID = f"{config.OUTPUTPATH}"

def setup():
    for path in config.PATHS:
        if not os.path.exists(path): os.makedirs(path)                  # If path don't exist, make it
    logging.info(f"Setup run at [{hour}:{minute}:{second} {month}/{day}/{year}]")

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
            logging.error(f"Routine Failed on {hour}:{minute}:{second} OS error: {0}".format(err))
            time.sleep(60)

# TODO If I use python 3.10, I can use a match case for user input on how often to run the TikTok routine

DAILY_SCHEDULED_TIME = "20:00"
schedule.every().day.at(DAILY_SCHEDULED_TIME).do(attemptRoutine)
attemptRoutine()    # Make one video right now
while True:         # and daily at the chosen time
    schedule.run_pending()  
    time.sleep(60)



