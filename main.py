import openai
import edge_tts
import asyncio
import requests
import configuration
import json

file_path = 'gptPrompt.txt'
with open(file_path, 'r') as file:
    prompt = file.read().strip()

def chatbot(prompt, question):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": prompt},
                      {"role": "user", "content": question}]
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        return f"An error occurred: {e}"

def generate_audio(text, audio_name="output.mp3"):
    try:
        voice = "en-GB-SoniaNeural"
        communicate = edge_tts.Communicate(text, voice)
        asyncio.run(communicate.save(f"Video Files/{audio_name}"))
    except Exception as e:
        print(f"An error occurred: {e}")

def generate_image(prompt, image_name):
    response = openai.Image.create(
        prompt=prompt,
        n=1,
        size="1024x1024"
    )
    image_url = response['data'][0]['url']
    image_data = requests.get(image_url).content
    with open(image_name, 'wb') as handler:
        handler.write(image_data)

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

for i, prompt in enumerate(image_prompts):
    image_name = f'Video Files/image-{i+1}.png'
    generate_image(prompt, image_name)

print(image_prompts)
