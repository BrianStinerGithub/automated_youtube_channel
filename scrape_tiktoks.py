from time import sleep
from TikTokApi import TikTokApi
import string
import random
import config
import urllib

def scrape_tiktoks():
    verifyFp = config.TIKTOKCOOKIE 
    did = ''.join(random.choice(string.digits) for _ in range(19))
    api = TikTokApi.get_instance(custom_verifyFP=verifyFp, custom_device_id=did)

    hashtag = config.HASHTAG
    tiktoks = api.by_hashtag(hashtag, 100)

    for tiktok in tiktoks:
        downloadaddress = tiktok['video']['downloadAddr']
        title = f"{tiktok['author']['nickname']}{tiktok['desc'][:10]}".translate(str.maketrans('', '', string.punctuation))
        download(downloadaddress, f"./TikTok/{hashtag}/{title}.mp4")


def download(url, file_name):
    with open(file_name, 'wb') as f:
        response = urllib.request.urlopen(url)
        f.write(response.read())

if "__main__" == __name__:
    print("Scraping Videos...")
    scrape_tiktoks()
    print("Scraped Videos!")



# for username in usernames:
#     tiktok = api.by_username(username, count=5)
#     download(tiktok['video']['downloadAddr'], f"./tiktoks/{hashtag}/{tiktok['author']['nickname']}{tiktok['desc'][:5]}.mp4")
#     sleep(5)

# mgtow = ["theKnowledgebros", "dr.dating", "the_real_advice","6footJay", "koldheartkamm", "moderndaiting", "saifiev", "motivationroom1", "qkoutes", "missiontomanhood", "garyvee", "stevenpapi_", "bgreat_quotes", "switchup18", "s7gray26", "lijah2x0", "blizzymanizzy", ".boysfeeltoo", "chakmah.deon", "prettyboyturbo_", "drunkie_6.7", "stateattire", "billionaireoption", "nathan.thomison", "5amdreamer", "geebmouth", "joshayy_14k", "blackvagabond1", "bulldogmindset", "ashtonisalpha", "thegrizzcaveofficial", "factsforrealationships", "godcoltonn", "toktate", "riseup.alex", "kamiosurgio", "fs.ryanwalker", "menshealthcoach", "the_redpill_experiment", "officialgic0e", "redpilllife", "stacks1400", "Joshsogravyy", "performance_potential", "thedreamarchitect", "theprincechuk", "johnnyoldenjr", "kamiosurgio", "amshighlights", "defundsimping", "cam.khs"]
# usernames = mgtow