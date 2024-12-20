import os
from instagrapi import Client
import logging
from time import sleep as sl
import requests
import schedule
import random
import pytz
from datetime import datetime, timedelta
from services.ai_services import image_detection, video_detection

cl = Client()

try:
    cl.login("avaskyler_", "ava@skyler#shaunbenedict")
except Exception as e:
    logging.error(f"Login failed: {e}")
    exit()

print("Logged In...")

log_file_path = './logs/media_ids.as'

counter = 0

def clears():
    os.system('rm ./files/*')

def reel_commenter(text, the_pk):
    cl.media_comment(the_pk, text)

def get_downloaded_media_ids(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            return set(line.strip() for line in file)
    return set()

def log_downloaded_media_id(file_path, media_id):
    with open(file_path, 'a') as file:
        file.write(f"{media_id}\n")

def post_processor():
    for a in ['s.shaunbenedict', 'dancingcharms.dc']:
        user_id = cl.user_id_from_username(str(a))
        downloaded_media_ids = get_downloaded_media_ids(log_file_path)

        media_items = cl.user_medias(user_id, amount=3)

        for media in media_items:
            if media.pk not in downloaded_media_ids:
                if media.media_type == 1:
                    photo_url = media.thumbnail_url
                    response = requests.get(photo_url)
                    with open(f"./files/{media.pk}.png", 'wb') as file:
                        file.write(response.content)
                    print(f"Downloaded photo: {media.pk}.png")
                    resp = image_detection(f"./files/{media.pk}.png")
                    reel_commenter(str(resp), media.pk)
                elif media.media_type == 2:
                    video_url = media.video_url
                    response = requests.get(video_url)
                    with open(f"./files/{media.pk}.mp4", 'wb') as file:
                        file.write(response.content)
                    print(f"Downloaded video: {media.pk}.mp4")            
                    resp = video_detection(f"./files/{media.pk}.mp4")
                    reel_commenter(str(resp), media.pk)
                log_downloaded_media_id(log_file_path, media.pk)
                cl.media_like(media.pk)
                sl(random.randrange(5,10))
            else:
                print(f"Media {media.pk} already downloaded.")
    if counter > 10:
        clears()

# def schedule_random_time():
#     london_tz = pytz.timezone('Europe/London')
#     now = datetime.now(london_tz)
#     start_time = now.replace(hour=7, minute=0, second=0, microsecond=0)
#     end_time = now.replace(hour=23, minute=59, second=59, microsecond=0)
#     random_time = start_time + timedelta(
#         seconds=random.randint(0, int((end_time - start_time).total_seconds()))
#     )
#     schedule_time = random_time.strftime("%H:%M:%S")
#     schedule.every().day.at(schedule_time).do(run_main)
#     print(f"Scheduled task at {schedule_time} London time")