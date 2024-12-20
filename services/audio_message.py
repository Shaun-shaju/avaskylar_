import os
from elevenlabs.client import ElevenLabs
from elevenlabs import save, Voice, VoiceSettings
from pydub import AudioSegment
from moviepy.video.VideoClip import ColorClip
from moviepy.audio.io.AudioFileClip import AudioFileClip

def convert(file,sender_id):
  audio = AudioSegment.from_mp3(file)
  video = ColorClip(size=(1280, 720), color=(0, 0, 0), duration=audio.duration_seconds)
  audio_clip = AudioFileClip(file)
  video = video.set_audio(audio_clip)
  video.write_videofile(f"./files/voice/audio_{sender_id}.mp4", codec="libx264", audio_codec="aac")
  return f"./files/voice/audio_{sender_id}.mp4"


client = ElevenLabs(
  api_key='sk_74e507ea806ff6a76eb4c8f676ceb1f4bcf2c994d641d0fc',
)

def audio_gen(tex, sender_id):
  hello = client.generate(
      text=tex,
      voice=Voice(
        voice_id='FGY2WhTYpPnrIDTdsKH5',
        settings=VoiceSettings(
            stability=0.8, similarity_boost=0.6, style=0.2, use_speaker_boost=True)
    )
  )

  save(hello, f"./files/voice/audio_{sender_id}.mp3")
  te = convert(f"./files/voice/audio_{sender_id}", sender_id)
  os.remove(f"./files/audio/audio_{sender_id}.mp3")
  return te
