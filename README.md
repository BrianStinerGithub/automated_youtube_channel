# Fully Automated Youtube Channel

Code to run a fully automated youtube that can run in the cloud to scrape content from TikTok, make a thumbnail, description, and complilation video with intro/outro/VFX/SFX then upload to youtube daily.

# Instructions

1. Download the Github Repository

2. If needed download and install python and pip

3. Install libraries with `pip install -r requirements.txt`

4. Get setup and create a Project with the Youtube API: https://developers.google.com/youtube/v3/quickstart/python
Be sure to follow it carefully, as it won't work if you don't do this part right.
Download your OATH file and name it as "googleAPI.json" in your project folder.

6. Go to TikTok and copy paste the cookie from your browser

7. In config.py edit the variables for your needs.

8. Run `python main.py` in your computer terminal (terminal or cmd). You have to sign in to your Youtube Account through the link the script will give you. It's going to ask you: "Please visit this URL to authorize this application:..." so you copy that link, paste it in your browser, and then sign into your Google account. 
Then paste the authentication code you get back into your terminal.

9. Enjoy your fully automated youtube channel! :) Note that for uploading public videos, you have to complete an audit for the Youtube API. 
See the note in the [Google Documentation](https://developers.google.com/youtube/v3/docs/videos/insert). 
Without this, you can only post private videos, but they approve everyone. Have fun!
