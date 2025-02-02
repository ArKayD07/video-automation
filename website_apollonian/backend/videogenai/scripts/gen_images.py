from openai import OpenAI
import requests
import configuration
import boto3

s3 = boto3.client('s3')
bucket_name = 'apollonianbucket'
client = OpenAI(api_key=configuration.openai_api_key)

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
    s3.upload_file(image_name, bucket_name, image_name)
