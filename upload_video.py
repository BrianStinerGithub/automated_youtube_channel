from simple_youtube_api.Channel import Channel
from simple_youtube_api.LocalVideo import LocalVideo
from simple_youtube_api.YouTube import YouTube
from config import *

client_secrets_file = "./assets/secrets.json"
scopes = ["https://www.googleapis.com/auth/youtube.upload"]
api_service_name = "youtube"
api_version = "v3"


def upload_video(
    account = ACCOUNTNAME,
    channel = CHANNELNAME,
    title = TITLE,
    description = DESCRIPTION,
    keywords = KEYWORDS,
    category = CATEGORY,
    privacyStatus = PRIVACYSTATUS,
    ):

    channel = Channel(account)
    channel.login("./assets/client_secret.json", "./assets/credentials.storage")

    # setting up the video that is going to be uploaded
    video = LocalVideo(file_path=OUTPUTPATH)

    # setting snippet
    video.set_title(title)
    video.set_description(description)
    video.set_tags(keywords)
    video.set_category(category)
    video.set_default_language("en-US")

    # setting status
    video.set_embeddable(True)
    video.set_license("creativeCommon")
    video.set_privacy_status(privacyStatus)
    video.set_public_stats_viewable(True)

    # setting thumbnail
    video.set_thumbnail_path(THUMBNAILPATH)

    # uploading video and printing the results
    video = channel.upload_video(video)
    print(video.id)
    print(video)

    # liking video
    video.like()
    
    # commenting on video


if __name__ == "__main__":
    print("Uploading video...")
    upload_video()
    print("Video was uploaded!")