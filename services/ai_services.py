from time import sleep as sl
import PIL
import google.generativeai as genai

genai.configure(api_key="AIzaSyBBxH_4EkVw0JG-Ha7-hIqsyQSlA1bUt7k")  

generation_config = {"temperature": 2}
initial_message = "You are Ava Skyler. You are acting as a 16yr old who is studying at Wilson, London. Your native place is at Kottayam, Kerala. You are to respond to the user like a teenager with emojis. You will talk like a GenZ person. You will comment on the attached media with mostly a positive note like example: 'That was fire! 🔥 You totally slayed it! 💃✨' or '✨ God’s Word always hits different 🙌💖 #Blessed #FaithGoals #VerseOfTheDay 📖💫'. You will limit the response to less than 1 sentence and mostly below 5 words."
caption = "Rate this content just like the given example"

def image_detection(filename):
    try:
        img = PIL.Image.open(filename)
        model = genai.GenerativeModel('gemini-1.5-pro', system_instruction=initial_message, generation_config=generation_config)
        response = model.generate_content([caption, img], stream=True)
        response.resolve()
        try:
            summary = response.text
        except (KeyError, IndexError) as e:
            print(f"Error extracting text: {e}")
        return summary
    except Exception as e:
        print(f"Error summarizing image with Gemini: {e}")
        return "An error occurred while processing the image."
    
def video_detection(filename):
    try:
        vid = genai.upload_file(path=filename)
        while vid.state.name == "PROCESSING":
            print('Waiting for video to be processed.')
            vid = genai.get_file(vid.name)
        if vid.state.name == "FAILED":
            raise ValueError(vid.state.name)
        print(f'Video processing complete: ' + vid.uri)
        model = genai.GenerativeModel('gemini-1.5-pro', system_instruction=initial_message, generation_config=generation_config)
        response = model.generate_content([caption, vid], stream=True)
        response.resolve()
        try:
            summary = response.text
        except (KeyError, IndexError) as e:
            print(f"Error extracting text: {e}")
        return summary
    except Exception as e:
        print(f"Error summarizing image with Gemini: {e}")
        return "An error occurred while processing the image."
