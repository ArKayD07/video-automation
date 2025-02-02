import edge_tts
import asyncio

def generate_audio(text, audio_name="output.mp3"):
    try:
        voice = "en-GB-SoniaNeural"
        communicate = edge_tts.Communicate(text, voice)
        asyncio.run(communicate.save(f"tmp/audio/{audio_name}"))
    except Exception as e:
        print(f"An error occurred: {e}")

def generate_tracks(scripts):
    for i in range(len(scripts)):
        audio_name = 'audio-' + str(i+1) + ".mp3"
        generate_audio(scripts[i], audio_name)