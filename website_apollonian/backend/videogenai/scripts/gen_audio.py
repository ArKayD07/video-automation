import asyncio
import boto3
import edge_tts
import configuration

s3 = boto3.client('s3')
bucket_name = 'apollonianbucket'

def generate_audio(text, audio_name="output.mp3"):
    try:
        voice = "en-GB-SoniaNeural"
        communicate = edge_tts.Communicate(text, voice)
        local_path = f"tmp/{audio_name}"
        asyncio.run(communicate.save(local_path))
        s3.upload_file(local_path, bucket_name, audio_name)
    except Exception as e:
        print(f"An error occurred: {e}")

def generate_tracks(scripts):
    for i in range(len(scripts)):
        audio_name = 'audio-' + str(i+1) + ".mp3"
        generate_audio(scripts[i], audio_name)
