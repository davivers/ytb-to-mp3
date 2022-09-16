from concurrent.futures import process
import requests
import json
from bs4 import BeautifulSoup
import pafy
import os
import sys
import subprocess
import time

link = input('Url: ')
start_time = time.time()
video_instance = pafy.new(link) #create pafy instance to find video title
song_name = video_instance.title #lookup video title utilizing pafy instance
api = 'https://cv.ytsilo.com/convert?link=' + link #append link to api
api_response = requests.get(api) #request api response
json_form_to_string = json.loads(api_response.text) # loading api response to string
slug_value = json_form_to_string['slug'] # finding slug value
conversion_down = 'https://ryin.info/' #conversion to mp3 site
append_slug = conversion_down + slug_value
conversion_link_lookup = requests.get(append_slug)
conversion_content = conversion_link_lookup.content
conversion_soup = BeautifulSoup(conversion_content, 'html.parser')
conversion_find_cid = conversion_soup.find('a', attrs={'class': 'btn btn-block btn-lg btn-success btn-download'})
cid = conversion_find_cid['download-href']
cid_download = requests.get(cid)
cid_download_status = cid_download.status_code

def download_song():
    if cid_download_status == 200:
        with open(f'{song_name}.mp3', 'wb') as f:
            f.write(cid_download.content)
        print("--- %s seconds ---" %(time.time() - start_time))
        print ("Done!")
    else:
        print ("404: Couldn't download file")

def check_song():
    if os.path.exists(os.path.join(os.getcwd(), f'{song_name}.mp3')) == True:
        print('Song already exists in current working directory...!')
        time.sleep(3)
        subprocess.call([sys.executable, os.path.realpath(__file__)] +
sys.argv[1:])
    else:
        download_song()

check_song()
download_song()
