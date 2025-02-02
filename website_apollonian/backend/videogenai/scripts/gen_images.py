import openai
import requests
from openai import OpenAI
import config as cfg


def generate_image(prompt, image_name):
    client = OpenAI(api_key=cfg.openai_api_key)
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

def generate_gallery(prompts):
    chapters = ['intro','definition','qresponse','conclusion']
    for i in range(len(chapters)):
        for j in range(len(prompts[i])):
            image_name = f'tmp/images/{chapters[i]}-{j + 1}.png'
            generate_image(prompts[i][j], image_name)
