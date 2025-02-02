import boto3
from openai import OpenAI
import edge_tts
import asyncio
import requests
import configuration
import json

client = OpenAI(api_key=configuration.openai_api_key)
s3 = boto3.client('s3')
bucket_name = 'apollonianbucket'
file_path = 'gptPrompt.txt'
with open(file_path, 'r') as file:
    prompt = file.read().strip()

def chatbot(prompt, question):
    try:
        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "developer", "content": prompt},
                {"role": "user","content": question}
            ]
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"An error occurred: {e}"

def generate_audio(text, audio_name="output.mp3"):
    try:
        voice = "en-GB-SoniaNeural"
        communicate = edge_tts.Communicate(text, voice)
        local_path = f"tmp/{audio_name}"
        asyncio.run(communicate.save(local_path))
        s3.upload_file(local_path, bucket_name, audio_name)
        print(f"Uploaded {audio_name} to S3 bucket {bucket_name}")
    except Exception as e:
        print(f"An error occurred: {e}")

def generate_image(prompt, image_name):
    response = client.images.generate(
        model='dall-e-3',
        prompt=prompt,
        n=1,
        size="1024x1024"
    )
    image_url = response.data[0].url
    image_data = requests.get(image_url).content
    with open(image_name, 'wb') as handler:
        handler.write(image_data)
    try:
        s3.upload_file(image_name, bucket_name, image_name)
        print(f"Uploaded {image_name} to S3 bucket {bucket_name}")
    except Exception as e:
        print(f"An error occurred: {e}")

category = input('Enter a category: ')
videoType = input('Enter a video type: ')
userInput = f"The video category is: {category}. The video type is: {videoType}."
response = chatbot(prompt, userInput)

print("Response from chatbot:\n", response)

chapter_strings = []
image_prompts = []

try:
    response_json = json.loads(response)
    for chapter in response_json['chapters']:
        chapter_strings.append(chapter['secondary text'])
        image_prompts.extend(chapter['image prompts'])
except json.JSONDecodeError as e:
    print(f"JSON decoding failed: {e}")
    exit(1)
except Exception as e:
    print(f"An unexpected error occurred: {e}")
    exit(1)

for i in range(len(chapter_strings)):
    audio_name = 'audio-' + str(i+1) + ".mp3"
    generate_audio(chapter_strings[i], audio_name)
for i in range(len(image_prompts)):
    image_name = 'tmp/image-' + str(i+1) + ".png"
    generate_image(image_prompts[i], image_name)
