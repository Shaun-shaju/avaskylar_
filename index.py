import os
from instagrapi import Client
import logging
from time import sleep as sl
import json
import requests
import schedule
from pydub import AudioSegment
from services.ai_services import image_detection, video_detection, chat, audio_detection

#Voice Keys
# sk_74e507ea806ff6a76eb4c8f676ceb1f4bcf2c994d641d0fc

#API KEYS
# AIzaSyBBxH_4EkVw0JG-Ha7-hIqsyQSlA1bUt7k
# AIzaSyAaLRTIPH8lsDjtDFH7RigfSY2ewDFs9cY
# AIzaSyAvGX-obpIT43hekTdggpkN2DVhf_RawaM

def save_processed_message_ids(processed_message_id, file_path="./logs/processed_ids.json"):
    with open(file_path, "w") as f:
        json.dump(processed_message_id, f)

cl = Client()

try:
    cl.login("avaskyler_", "ava@skyler#shaunbenedict")
    print("Done")
except Exception as e:
    logging.error(f"Login failed: {e}")
    exit()

# Load processed_message_ids from a JSON file
def load_processed_message_ids(file_path="./logs/processed_ids.json"):
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            return json.load(f)
    return []


print("Logged In...")
processed_message_ids = load_processed_message_ids()

def fetch_and_respond():
    global processed_message_ids  # Ensure we can access the global set
    try:
        threads = cl.direct_threads(amount=10)
        for thread in threads:
            if not thread.messages:
                continue
            last_message = thread.messages[0]  # Get the most recent message
            message_id = last_message.id
            sender_id = last_message.user_id

            if message_id in processed_message_ids or str(sender_id) == str(cl.user_id):
                continue  # Skip if already processed or sent by the bot

            if last_message.item_type == "text":
                message_text = last_message.text
                print(f"New message from {sender_id}: {message_text}")
                if message_text:
                    reply = chat(message_text, sender_id)
                else:
                    reply = "Sorry, I didn't understand that. Can you rephrase?"

            elif last_message.item_type in ["media", "visual_media", "raven_media"]:
                # Extract URLs
                urls = [candidate['url'] for candidate in last_message.visual_media['media']['image_versions2']['candidates']]
                photo_content = requests.get(urls[0]).content
                file_path = f"./files/media/photo_{message_id}.jpg"
                with open(file_path, "wb") as f:
                    f.write(photo_content)
                print(f"Downloaded photo: photo_{message_id}.jpg")
                reply = image_detection(file_path, sender_id)
            elif last_message.item_type == "voice_media":
                audio_url = last_message.media.audio_url
                audio_content = requests.get(audio_url).content
                mp4_path = f"./files/audio/audio_{message_id}.mp4"
                mp3_path = f"./files/audio/audio_{message_id}.mp3"
                with open(mp4_path, "wb") as f:
                    f.write(audio_content)
                audio = AudioSegment.from_file(mp4_path, format="mp4")
                audio.export(mp3_path, format="mp3")
                print(f"Converted audio to MP3: {mp3_path}")
                os.remove(mp4_path)
                reply = audio_detection(mp3_path, sender_id)
            elif last_message.item_type == 'clip':
                video_url = last_message.clip.video_url
                response = requests.get(video_url)
                with open(f"./files/reels/video_clip{sender_id}.mp4", 'wb') as file:
                        file.write(response.content)
                print(f"Downloaded video: ./files/reels/video_clip{sender_id}.mp4")
                reply = video_detection(f"./files/reels/video_clip{sender_id}.mp4", sender_id)
            else:
                print(last_message.item_type)
                print("\n\n")
                #reply = "I currently can't process this type of message. Stay tuned for updates!"
            if last_message.item_type != "voice_media":
                cl.direct_send(reply, [sender_id])
            else:
                cl.direct_send_video(path= reply, user_ids= [sender_id])
            processed_message_ids.append(message_id)  # Mark as processed
        save_processed_message_ids(processed_message_ids)

    except Exception as e:
        logging.error(f"Error fetching or responding to messages: {e}")

                
        save_processed_message_ids(processed_message_ids)

    except Exception as e:
        logging.error(f"Error fetching or responding to messages: {e}")

# Schedule the chatbot
schedule.every(10).seconds.do(fetch_and_respond)

print("Chatbot running... Press Ctrl+C to stop.")

while True:
    schedule.run_pending()
    sl(1)