import asyncio
import boto3
import edge_tts
import configuration

s3 = boto3.client('s3')
bucket_name = 'apollonianbucket'
voices = {'friendly': 'en-GB-RyanNeural', 
          'positive': 'en-US-AriaNeural', 
          'confident': 'en-US-EricNeural', 
          'professional': 'en-GB-SoniaNeural', 
          'cute': 'en-US-AnaNeural', 
          'authority': 'en-US-ChristopherNeural', 
          'reliable': 'en-US-EricNeural', 
          'humorous': 'zh-CN-liaoning-XiaobeiNeural', 
          'rational': 'en-US-SteffanNeural',
          'passionate': 'en-US-GuyNeural',
          'considerate': 'en-US-JennyNeural',
          'pleasant': 'en-US-MichelleNeural',
          'lively': 'en-US-RogerNeural'}

def generate_audio(text, tone, audio_name="output.mp3"):
    try:
        voice = voices[tone]
        communicate = edge_tts.Communicate(text, voice)
        local_path = f"Video Files/{audio_name}"
        asyncio.run(communicate.save(local_path))
        s3.upload_file(local_path, bucket_name, audio_name)
        print(f"Uploaded {audio_name} to S3 bucket {bucket_name}")
    except Exception as e:
        print(f"An error occurred: {e}")

def generate_tracks(scripts):
    for i in range(len(scripts)):
        audio_name = 'audio-' + str(i+1) + ".mp3"
        generate_audio(scripts[i], audio_name)
