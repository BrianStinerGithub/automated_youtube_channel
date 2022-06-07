from simple_youtube_api.Channel import Channel
from simple_youtube_api.LocalVideo import LocalVideo
from simple_youtube_api.YouTube import YouTube
from config import *
import logging

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
    video_path = OUTPUTPATH,
    ):

    channel = Channel()
    channel.login("./assets/secrets.json", "./assets/credentials.storage")

    # setting up the video that is going to be uploaded
    video = LocalVideo(file_path=video_path)

    # setting snippet
    video.set_title(title)
    video.set_description(description)
    video.set_tags(list(keywords))
    video.set_category(category)
    video.set_default_language("en-US")

    # setting status
    video.set_embeddable(True)
    video.set_license("creativeCommon")
    video.set_privacy_status(privacyStatus)
    video.set_public_stats_viewable(True)
    video.set_made_for_kids(False)

    # setting thumbnail
    video.set_thumbnail_path("./assets/Template.png")            

    # Upload video
    video = channel.upload_video(video)
    logging.info(f"Video uploaded: {video.title} - {video.id} [{MONTH}/{NOW.day}/{NOW.year}]")

    # Like video
    video.like()


if __name__ == "__main__":
    upload_video()