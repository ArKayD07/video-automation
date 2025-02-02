from openai import OpenAI
import requests
import config
client = OpenAI(api_key=config.openai.api_key)

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