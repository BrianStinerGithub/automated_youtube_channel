from turtle import title
from moviepy.editor import VideoFileClip, concatenate_videoclips
from moviepy.video.fx.resize import resize
import os
from os.path import isfile, join
import random
import shutil 
from collections import defaultdict
import config
import psutil
from playsound import playsound

VideoFileClip.resize = resize

def extractAcc(filepath):
    try:
        s = filepath.split("/")[-1].split("-")
        acc = "-".join(s[1:(2+(len(s) - 4))])
        return acc
    except:
        return ""

# generateTimeRange converts float seconds to a range of form @MM:SS
def generateTimeRange(duration, clipDuration):
    preHour = int(duration / 60)
    preMin = int(duration % 60)
    preTime = str(preHour // 10) + str(preHour % 10) + ":" + str(preMin // 10) + str(preMin % 10)

    duration += clipDuration
    postHour = int(duration / 60)
    postMin = int(duration % 60)
    postTime = str(postHour // 10) + str(postHour % 10) + ":" + str(postMin // 10) + str(postMin % 10)

    #return "@" + preTime + " - " + "@" + postTime
    return "@" + preTime
    
# makeCompilation takes videos in a folder and creates a compilation with max length totalVidLength
def makeCompilation(path = "",
                    introName = '',
                    outroName = '',
                    totalVidLength = 14*60,
                    maxClipLength = 60,
                    minClipLength = 5,
                    outputFile = "output.mp4"):

    allVideos = []
    seenLengths = defaultdict(list)
    totalLength = 0
    for fileName in os.listdir(path):
        
        filePath = join(path, fileName);
        if isfile(filePath) and fileName.endswith(".mp4"):
            print(fileName)
            if psutil.virtual_memory()[2] > 99:
                print(f"\n!\n!\nNot enough memory to continue: {psutil.virtual_memory()[2]}%\n!\n!")
                break

            # Destination path  
            clip = VideoFileClip(filePath)
            clip = clip.resize(width=1920)
            clip = clip.resize(height=1080)
            duration = clip.duration
            print(duration)
            if duration <= maxClipLength and duration >= minClipLength:
                allVideos.append(clip)
                seenLengths[duration].append(fileName)
                totalLength += duration
                print(totalLength)
    
    print("Total Length: " + str(totalLength))

    random.shuffle(allVideos)

    duration = 0
    # Add intro vid
    videos = []
    if introName != '':
        introVid = VideoFileClip("./" + introName)
        videos.append(introVid)
        duration += introVid.duration
    
    description = ""
    # Create videos
    for clip in allVideos:
        timeRange = generateTimeRange(duration, clip.duration)
        acc = extractAcc(clip.filename)
        description += timeRange + " : @" + acc + "\n"
        duration += clip.duration 
        videos.append(clip)
        print(duration)
        if duration >= totalVidLength:
            # Just make one video
            break
    
    # Add outro vid
    if outroName != '':
        outroVid = VideoFileClip("./" + outroName)
        videos.append(outroVid)
        duration += outroVid.duration

    finalClip = concatenate_videoclips(videos, method="compose")

    tmp_audio_path = "./tmp/tempaudiofile.m4a"

    #print(description)
    # Create compilation
    print(outputFile)
    finalClip.write_videofile(outputFile, temp_audiofile=tmp_audio_path, remove_temp=True, 
    codec="mpeg4", audio_codec="aac", audio_bitrate="192k", 
    preset="ultrafast", threads=8, verbose = True, logger=None)

    return description


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



# if __name__ == "__main__":
inputpath, website, hashtag = inputpathreader(config.INPUTPATH) #os.path.normpath("./TikTok/Red Pill/Confirmed")) # C:\Users\maste\OneDrive\Desktop\AutomatedVideos\automated_youtube_channel
title = f"{config.HOOK} | {hashtag} {website} Compilation EP {config.NUM}"



makeCompilation(path = inputpath, 
                introName = config.INTROPATH,
                outroName = config.OUTROPATH,
                totalVidLength = config.VIDEO_LENGTH,
                maxClipLength = config.MAX_CLIP_LENGTH,
                minClipLength = config.MIN_CLIP_LENGTH,
                outputFile = config.OUTPUTPATH)

print(f"\n{title} | Finished")
print(f"\nPlaying alarm sound")
playsound('Alert.m4a')
# print(f"\n{description}")
