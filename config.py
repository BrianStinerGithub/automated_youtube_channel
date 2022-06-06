
TIKTOKCOOKIE = "verify_9cd3ed1f0c495e641d3eafbe4384085f"    # Grab the s_v_web_id cookie from browser and paste here
HASHTAG = "[Fuzzy Hats]"                                    # Hashtag for your channel 

# Youtube information
ACCOUNTNAME = "Masterdiasastermail@gmail.com"
CHANNELNAME = "UnconventionalWisdom"
TITLE = "I made an automatic video, this is the result"
DESCRIPTION = "I made the video with python using the TikTok API, the YouTube API, MoviePy, CV2, and Google API. I hope you enjoy it!"
KEYWORDS = "supercool", "cool", "tiktok", "tiktoktiktok", "tiktoktiktoktiktok"
CATEGORY = 22
PRIVACYSTATUS = "public"

# 15 min temp limit. TikTok lengths are between min-max seconds.
VIDEO_LENGTH = 14*60
MAX_CLIP_LENGTH = 100
MIN_CLIP_LENGTH = 5
# Dates and times
import datetime
now = datetime.datetime.now()
NOW = now
MONTH = {
    1: "January",   2: "Febuary",   3: "March",
    4: "April",     5: "May",       6: "June",
    7: "July",      8: "August",    9: "September",
    10: "October",  11: "November", 12: "December"
}[NOW.month]

# Paths
timecodeFolder =f"{HASHTAG}-{MONTH}_{NOW.day}_{NOW.year}"
OUTPUTPATH =    f"./assets/videos/Created/{timecodeFolder}"
TIKTOKPATH =    f"./assets/videos/TikTok/{timecodeFolder}"
INTROPATH =     f"./assets/videos/Intro"
OUTROPATH =     f"./assets/videos/Outro"
THUMBNAILPATH = f"./assets/thumbnails/{timecodeFolder}"
BACKGROUNDPATH =f"./assets/thumbnails"
PATHS = {
    OUTPUTPATH, TIKTOKPATH, INTROPATH, OUTROPATH, THUMBNAILPATH
}





