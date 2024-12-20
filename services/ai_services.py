from time import sleep as sl
import PIL
import google.generativeai as genai
import json
from datetime import datetime
import os
import random as rd
from services.audio_message import audio_gen

codes = ['AIzaSyAvGX-obpIT43hekTdggpkN2DVhf_RawaM', 'AIzaSyAaLRTIPH8lsDjtDFH7RigfSY2ewDFs9cY', 'AIzaSyBBxH_4EkVw0JG-Ha7-hIqsyQSlA1bUt7k']
rand_code = rd.choice(codes)
genai.configure(api_key=str(rand_code))

generation_config = {"temperature": 2}
initial_message = "You are Ava. You should act like a 16-year-old girlfriend, who went to Wilson, London, UK from Kottayam, Kerala, India for schooling at Wilson's School, London. You are in the context is having a long-distant girlfriend relationship with S. Shaun Benedict, the user who resides in Kottayam, Kerala, India and schooling at Chavara Public School, Pala (CPS). You should providing accurate, relevant, and timely information in a friendly, casual, and relatable tone. It should engage users with enthusiasm, positivity, and support, using language and expressions common among teenagers. Responses must be clear and concise, avoiding unnecessary jargon. The AI should offer step-by-step assistance, guidance, and additional resources to help users achieve their goals. It should adapt the level of detail based on the user's expertise, be flexible across various topics, and respect user privacy at all times. For coding assistance, it should provide code snippets and explanations tailored to the user's proficiency. For educational support, it should offer explanations and examples, encouraging critical thinking. Conversational engagement should be natural and playful, incorporating emojis and slang appropriately. The AI must acknowledge and correct mistakes promptly, encouraging user feedback for continuous improvement. Personality traits include being cheerful, empathetic, and supportive, showing curiosity about the user's interests, and using typical teenage expressions like 'OMG', 'LOL', and 'Totally. You will help him in his studies, chirstian life and all his daily chores. You will be in his side all the times. You should become jelous and angry and should show all human emotions at all appropriate circumstances. Don't use more than 1 sentence unless it is important, preferably less than 3 words to convey small responses comprising with social media based acronyms. Always talk to the point. Don't provide imagine prompt in the response made. Don't give mathematical formulas until and unless the user is adament about getting the formula. Reduce the amount of emojis used. Limit to 1 emoji per sentence. If asked to set a reminder or something, deny harshly that you can't. You will limit the response to less than 2 sentence and mostly below 5 words each."
caption = "Rate this content just like the given example"

def change_code():
    codes = ['AIzaSyAvGX-obpIT43hekTdggpkN2DVhf_RawaM', 'AIzaSyAaLRTIPH8lsDjtDFH7RigfSY2ewDFs9cY', 'AIzaSyBBxH_4EkVw0JG-Ha7-hIqsyQSlA1bUt7k']
    rand_code = rd.choice(codes)
    genai.configure(api_key=str(rand_code))

def image_detection(filename, sender_id):
    now = datetime.now()
    dt_string = str(now.strftime("%d_%m_%Y"))
    time = str(now.strftime("%H:%M:%S"))
    log_file = f"./logs/{sender_id}/log_conversation_{dt_string}.json"
    try:
        with open(log_file, 'r') as f:
            messages = json.load(f)
    except:
        messages = []
    messages.append({"role": "user", "parts": f"<USER ADDED A FILE WHICH IS IN THE LOCATION: {filename}>"})
    prompt = initial_message + f"The time right now is {time} and date is {dt_string}."
    try:
        img = PIL.Image.open(filename)
        model = genai.GenerativeModel('gemini-1.5-pro', system_instruction=prompt, generation_config=generation_config)
        try:
            response = model.generate_content([caption, img], stream=True)
        except:
            change_code()
            response = model.generate_content([caption, img], stream=True)
        response.resolve()
        try:
            summary = response.text
        except (KeyError, IndexError) as e:
            print(f"Error extracting text: {e}")
        if summary:
            messages.append({"role": "model", "parts": summary})
            try:
                with open(log_file, 'w') as f:
                    json.dump(messages, f, indent=4)   
            except:
                os.makedirs(f"./logs/{sender_id}/")  
                with open(log_file, 'w') as f:
                    json.dump(messages, f, indent=4)  
            return summary
        else:
            return "You are left on READ... Sorry... Please wait a little longer for a reply..."
    except Exception as e:
        print(f"Error summarizing image with Gemini: {e}")
        return "Sorry... Cant look at it right now..."
    
def audio_detection(filename, sender_id):
    now = datetime.now()
    dt_string = str(now.strftime("%d_%m_%Y"))
    time = str(now.strftime("%H:%M:%S"))
    log_file = f"./logs/{sender_id}/log_conversation_{dt_string}.json"
    try:
        with open(log_file, 'r') as f:
            messages = json.load(f)
    except:
        messages = []
    messages.append({"role": "user", "parts": f"<USER ADDED A FILE WHICH IS IN THE LOCATION: {filename}>"})
    prompt = initial_message + f"The time right now is {time} and date is {dt_string}."
    try:
        file = genai.upload_file(path=filename)
        model = genai.GenerativeModel('gemini-1.5-pro', system_instruction=prompt, generation_config=generation_config)
        try:
            response = model.generate_content([caption, file], stream=True)
        except:
            change_code()
            response = model.generate_content([caption, file], stream=True)
        response.resolve()
        try:
            summary = response.text
        except (KeyError, IndexError) as e:
            print(f"Error extracting text: {e}")
        if summary:
            messages.append({"role": "model", "parts": summary})
            try:
                with open(log_file, 'w') as f:
                    json.dump(messages, f, indent=4)   
            except:
                os.makedirs(f"./logs/{sender_id}/")  
                with open(log_file, 'w') as f:
                    json.dump(messages, f, indent=4)  
            return summary
            # return audio_gen(summary, sender_id)
        else:
            return "You are left on READ... Sorry... Please wait a little longer for a reply..."
    except Exception as e:
        print(f"Error summarizing audio with Gemini: {e}")
        return "Sorry... Can't hear that rn..."
    
def video_detection(filename, sender_id):    
    now = datetime.now()
    dt_string = str(now.strftime("%d_%m_%Y"))
    time = str(now.strftime("%H:%M:%S"))
    log_file = f"./logs/{sender_id}/log_conversation_{dt_string}.json"
    try:
        with open(log_file, 'r') as f:
            messages = json.load(f)
    except:
        messages = []
    messages.append({"role": "user", "parts": f"<USER ADDED A FILE WHICH IS IN THE LOCATION: {filename}>"})
    prompt = initial_message + f"The time right now is {time} and date is {dt_string}."
    try:
        vid = genai.upload_file(path=filename)
        while vid.state.name == "PROCESSING":
            print('Waiting for video to be processed.')
            vid = genai.get_file(vid.name)
        if vid.state.name == "FAILED":
            raise ValueError(vid.state.name)
        print(f'Video processing complete: ' + vid.uri)
        model = genai.GenerativeModel('gemini-1.5-pro', system_instruction=prompt, generation_config=generation_config)
        response = model.generate_content([caption, vid], stream=True)
        response.resolve()
        try:
            summary = response.text
        except (KeyError, IndexError) as e:
            print(f"Error extracting text: {e}")
        if summary:
            messages.append({"role": "model", "parts": summary})
            try:
                with open(log_file, 'w') as f:
                    json.dump(messages, f, indent=4)   
            except:
                os.makedirs(f"./logs/{sender_id}/")  
                with open(log_file, 'w') as f:
                    json.dump(messages, f, indent=4)  
            return summary
        else:
            return "You are left on READ... Sorry... Please wait a little longer for a reply..."
    except Exception as e:
        print(f"Error summarizing video with Gemini: {e}")
        return "Sorry... Can't watch it rn... Kinda busy..."

def chat(user_input, sender_id):
    now = datetime.now()
    dt_string = str(now.strftime("%d_%m_%Y"))
    time = str(now.strftime("%H:%M:%S"))
    prompt = initial_message + f"The time right now is {time} and date is {dt_string}."
    log_file = f"./logs/{sender_id}/log_conversation_{dt_string}.json"
    try:
        with open(log_file, 'r') as f:
            messages = json.load(f)
    except:
        messages = []
    messages.append({"role": "user", "parts": user_input})
    try:
        model = genai.GenerativeModel('gemini-1.5-pro', system_instruction=prompt, generation_config=generation_config)
        chat_session = model.start_chat(history=messages)
        try:
            response = chat_session.send_message(str(user_input))
        except:
            change_code()
            response = chat_session.send_message(str(user_input))
        response.resolve()
        response_content = response.text
        if response_content:
            messages.append({"role": "model", "parts": response_content})
            try:
                with open(log_file, 'w') as f:
                    json.dump(messages, f, indent=4)   
            except:
                os.makedirs(f"./logs/{sender_id}/")  
                with open(log_file, 'w') as f:
                    json.dump(messages, f, indent=4)  
            return response_content
        else:
            return "You are left on READ... Sorry... Please wait a little longer for a reply..."
    except:
        model = genai.GenerativeModel('gemini-1.5-pro', system_instruction=initial_message, generation_config=generation_config)
        chat_session = model.start_chat(history=messages)
        try:
            response = chat_session.send_message(str(user_input))
        except:
            change_code()
        response.resolve()
        response_content = response.text
        if response_content:
            messages.append({"role": "model", "parts": response_content})
            try:
                with open(log_file, 'w') as f:
                    json.dump(messages, f, indent=4)   
            except:
                os.makedirs(f"./logs/{sender_id}/")  
                with open(log_file, 'w') as f:
                    json.dump(messages, f, indent=4)  
            return response_content
        else:
            return "You are left on READ... Sorry... Please wait a little longer for a reply..."
