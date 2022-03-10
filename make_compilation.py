from turtle import back, title
from moviepy.editor import ImageClip, VideoFileClip, CompositeVideoClip, concatenate_videoclips
from moviepy.video.fx.resize import resize
import os
from os.path import isfile, join
from random import shuffle
from collections import defaultdict
import config
import psutil
import create_thumbnail as ct
import tqdm
from PIL import Image
import string

VideoFileClip.resize = resize

def extractAcc(filepath):
        name = filepath.split("\\")[-1].split("_")[0]
        return ''.join((filter(lambda x: x in string.printable, name)))

# generateTimeRange converts float seconds to a range of form @MM:SS
def generateTimeRange(duration):
    Hour = int(duration / 60)
    Min = int(duration % 60)
    Time = str(Hour // 10) + str(Hour % 10) + ":" + str(Min // 10) + str(Min % 10)
    return Time
    
# makeCompilation takes videos in a folder and creates a compilation of max length
def makeCompilation(path = config.INPUTPATH,
                maxVidLength = config.VIDEO_LENGTH,
                maxClipLength = config.MAX_CLIP_LENGTH,
                minClipLength = config.MIN_CLIP_LENGTH):

    allVideos = []
    totalLength = 0
    for fileName in os.listdir(path):
        
        filePath = join(path, fileName);
        if isfile(filePath) and fileName.endswith(".mp4"):
            print(fileName)

            #Prevent memory crash
            if psutil.virtual_memory()[2] > 99:
                print(f"\n!\nNot enough memory to continue: {psutil.virtual_memory()[2]}%\n!")
                break

            # Destination path  
            clip = VideoFileClip(filePath)
            clip = clip.resize(width=1920)
            clip = clip.resize(height=1080)
            duration = clip.duration
            if duration <= maxClipLength and duration >= minClipLength:
                allVideos.append(clip)
                totalLength += duration
                print(totalLength)
                if totalLength >= maxVidLength:
                    writeCompilation(allVideos)
                    allVideos = []
                    totalLength = 0
    
    print("Total Length: " + str(totalLength))
    writeCompilation(allVideos)

def writeCompilation(allVideos,  
                introName = config.INTROPATH,
                outroName = config.OUTROPATH,
                outputFile = config.OUTPUTPATH):

    shuffle(allVideos)
    duration = 0
    videos = []
    description = ""
    TM = ct.ThumbnailMaker()
    background = ImageClip("./Thumbnail/Template.png")

    # Add intro video
    if introName != '':
        introVid = VideoFileClip("./" + introName)
        allVideos.prepend(introVid)

    # Add outro vid
    if outroName != '':
        outroVid = VideoFileClip("./" + outroName)
        allVideos.append(outroVid)
    
    # Add clips, descriptions, and thumbnails
    for clip in allVideos:
        description += generateTimeRange(duration) + " - " + extractAcc(clip.filename) + "\n"
        duration += clip.duration 
        cclip = CompositeVideoClip([background.set_duration(clip.duration), clip.set_position((background.w/2 - clip.w/2, 0))])
        videos.append(cclip)
        TM.compare_topn(clip)

    # Create compilation
    finalClip = concatenate_videoclips(videos, method="compose")
    tmp_audio_path = "./tmp/tempaudiofile.m4a"
    finalClip.set_memoize(True)
    finalClip.write_videofile("output.avi", temp_audiofile=tmp_audio_path, remove_temp=True, 
     codec="png", audio_codec="aac", audio_bitrate="192k", 
     preset="ultrafast", threads=8, verbose = True, logger=None)

    # Create thumbnail 
    TM.make_thumbnail().save("./tmp/thumbnail.png")

    # Create description 
    with open("./tmp/description.txt", "w") as f:
        f.write(description)



# Takes a path like this: ./website/genre/Confirmed and seperates out TikTok, Funny, and Confirmed into their own variables
def inputpathreader(path = None): 
    if path == None:
        path = input("Enter path to videos: ")
    if not os.path.exists(path):
        print("Path does not exist")
        return None
    website, hashtag, confirmed = path[2:].split("/")
    if confirmed != "Confirmed":
        print("Path does not end with confirmed")
        return None
    return path, website, hashtag


if __name__ == "__main__":
    inputpath, website, hashtag = inputpathreader(config.INPUTPATH) #os.path.normpath("./TikTok/Red Pill/Confirmed")) # C:\Users\maste\OneDrive\Desktop\AutomatedVideos\automated_youtube_channel
    title = f"{config.HOOK} | {hashtag} {website} Compilation EP {config.NUM}"
    print("Making Compilation...")
    makeCompilation()
    print(f"\n{title} | Finished")


# print(f"\nPlaying alarm sound")
# playsound('Alert.m4a')
# print(f"\n{description}")
