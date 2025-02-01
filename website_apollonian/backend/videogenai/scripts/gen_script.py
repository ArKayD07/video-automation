import openai
import json
import config as cfg
from openai import OpenAI

def printLog(chapters,imgs):
    msg = f"Intro: {chapters[0]}\n"
    msg += f"> image prompts: {imgs[0]}\n"
    msg += f"Definition: {chapters[1]}\n"
    msg += f"> image prompts: {imgs[1]}\n"
    msg += f"Response to the Question: {chapters[2]}\n"
    msg += f"> image prompts: {imgs[2]}\n"
    msg += f"Conclusion: {chapters[3]}\n"
    msg += f"> image prompts: {imgs[3]}"
    
    print(msg)

def readSysPrompt(file_path):
    with open(file_path, 'r') as file:
        raw = file.read().strip()
    
    return raw

def parseJSON(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    
    return data

def chatbot(system, user):
    try:
        client = OpenAI(api_key=cfg.openai.api_key)
        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system},
                {"role": "user","content": user}
            ]
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"An error occurred: {e}"

def generateScript():
    sysPrompt_raw = readSysPrompt('sysPrompt.txt')
    category = input('gen_script > Enter a category: ')
    videoType = input('gen_script > Enter a video type: ')
    usrPrompt = f"The video category is: {category}. The video type is: {videoType}."

    subprompts = []
    titles_sps = ['intro','definition','response-to-the-question','conclusion']
    subprompts_raw = parseJSON('subprompts.txt')
    for title in titles_sps:
        subprompts.append(subprompts_raw[videoType][title]) 

    sysPrompt = sysPrompt_raw.format(sp1=subprompts[0],sp2=subprompts[1],sp3=subprompts[2],sp4=subprompts[3])
    
    response = chatbot(sysPrompt,usrPrompt)

    # PARSE RESPONSE FROM CHATGPT
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

