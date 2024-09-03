import yt_dlp
import requests, json, os
from jigsawstack import JigsawStack, JigsawStackError as err
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('JIGSAW_STACK_API_KEY')
jigsawstack = JigsawStack(api_key)

def download_audio(link):
  ydl_opts = {
    'extract_audio': True, 
    'format': 'bestaudio/best',
    'cookies-from-browser': 'cookies.txt',
    'outtmpl': 'temp',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '128',
    }],
}

  with yt_dlp.YoutubeDL(ydl_opts) as video:
    info_dict = video.extract_info(link, download = True)
    # video_title = info_dict['title']
    video.download(link)    
    print("Successfully Downloaded")

def jss_stt(url):
    response = jigsawstack.audio.speech_to_text({"url": url})

    return response

def upload_temp_files(file):
    url = "https://tmpfiles.org/api/v1/upload"
    files = {'file': open(file, 'rb')}
    # headers = {"Content-Type": "application/json", "x-api-key": api_key}    
    res = requests.post(url, files=files )
    json_data = json.loads(res.content)
    # audio_url = data["url"]
    data = json_data["data"]
    raw_url = data["url"]
    site_url = raw_url[0:21]
    remainder = raw_url[21:]
    download_url = site_url + "dl/" +remainder
    return download_url

