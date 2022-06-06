from moviepy.editor import ImageClip, VideoFileClip, CompositeVideoClip, concatenate_videoclips
from os.path import isfile, join
from config import *
import logging
import os
import psutil
import create_thumbnail as ct
import string

def extractAcc(filepath):
        name = filepath.split("\\")[-1].split("_")[0]
        return ''.join((filter(lambda x: x in string.printable, name)))

# generateTimeRange converts float seconds to a range of form @HH:MM
def generateTimeRange(duration):
    hour, minute, second = int(duration / 60), int(duration % 60), int(duration % 1 * 60)
    if hour > 0:
        return f"@{hour:02d}:{minute:02d}:{second:02d}"
    return f"@{minute:02d}:{second:02d}"

def prepareClip(clip):
    clip = clip.resize(width=1920)
    clip = clip.resize(height=1080)
    background = ImageClip(f"{BACKGROUNDPATH}/Template.png")
    if os.path.isfile(background):
        return CompositeVideoClip([background.set_duration(clip.duration), clip.set_position((background.w/2 - clip.w/2, 0))])
    return clip 

# makeCompilation takes videos in a folder and creates a compilation of max length
def makeCompilation(inputpath = TIKTOKPATH,                                                                 #
                maxVidLength = VIDEO_LENGTH,                                                                #
                maxClipLength = MAX_CLIP_LENGTH,                                                            #
                minClipLength = MIN_CLIP_LENGTH):                                                           # This is a big function that reads all
    logging.info("Creating Compilation...")                                                                 # TikToks in the folder except too short or long ones.
    videos = []                                                                                             # We compare them with resnet for clickability for the thumbnail.                                 
    totalDuration = 0                                                                                       # We correct the aspect ratio and add a background image.
    TM = ct.ThumbnailMaker()                                                                                # When compilation is long enough, it shuffles the order
    for fileName in os.listdir(inputpath):                                                                  # We then add an intro and outro if they exist.
        filePath = join(inputpath, fileName)                                                                # We write the new video to the output path and
        if isfile(filePath) and fileName.endswith(".mp4"):                                                  # save the created thumbnail and description.
            #Prevent memory crash at 100% ram usage                                                         #            
            if psutil.virtual_memory()[2] > 99:                                                             #    
                logging.warning(f"\n!\nNot enough memory to continue: {psutil.virtual_memory()[2]}%\n!\n")  #
                break
            # Read in video, resize, add background, 
            # compare with resnet, and add to videos list 
            # if not too long or too short
            tiktok = VideoFileClip(filePath)
            TM.compare_topn(tiktok)
            tiktok = prepareClip(tiktok)
            duration = tiktok.duration
            if duration <= maxClipLength and duration >= minClipLength:
                videos.append(tiktok)
                totalDuration += duration
            if totalDuration >= maxVidLength:
                break
            logging.info(f"{fileName} added")
    
    videos.shuffle()

    timer = 0 
    description = ""

    # Add intro video 
    intro = f"{INTROPATH}/Intro.mp4"
    if  os.path.isfile(intro):
        introVid = VideoFileClip(intro)
        videos.prepend(introVid)

    # Add outro vid
    outro = f"{OUTROPATH}/Outro.mp4"
    if os.path.isfile(outro):
        outroVid = VideoFileClip(outro)
        videos.append(outroVid)
    
    # Create description
    for vid in videos:
        description += generateTimeRange(timer) + " - " + extractAcc(vid.filename) + "\n"
        timer += vid.duration
    with open("./tmp/description.txt", "w") as f:
        f.write(description)

    # Create thumbnail 
    TM.make_thumbnail().save(f"{THUMBNAILPATH}/output.png")

    # Create new video
    finalClip = concatenate_videoclips(videos, method="compose")
    tmp_audio_path = "./tmp/tempaudiofile.m4a"
    finalClip.set_memoize(True)
    finalClip.write_videofile(f"{OUTPUTPATH}/output.avi", temp_audiofile=tmp_audio_path, remove_temp=True, 
        codec="png", audio_codec="aac", audio_bitrate="192k", 
        preset="ultrafast", threads=8, verbose=True, logger=None)

    logging.info("Compilation complete")
    logging.info("Total Length: " + str(totalDuration))
    
if __name__ == "__main__":
    makeCompilation()

