import openai
import json
import os
import re
import config as cfg
from openai import OpenAI

def wcount(text):
    count = len(re.findall(r'\w+',text))
    return count

def printLog(chapters,imgs):
    msg = "Diagnostics:\n"
    msg += f"> word count: {wcount(chapters[0]) + wcount(chapters[1]) + wcount(chapters[2]) + wcount(chapters[3])}\n"
    msg += f"> img_prompts[intro]: {len(imgs[0])}\n"
    msg += f"> img_prompts[definition]: {len(imgs[1])}\n"
    msg += f"> img_prompts[qresponse]: {len(imgs[2])}\n"
    msg += f"> img_prompts[conclusion]: {len(imgs[3])}\n"
    
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
        client = OpenAI(api_key=cfg.openai_api_key)
        completion = client.chat.completions.create(
            response_format={"type":"json_object"},
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system},
                {"role": "user","content": user}
            ]
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"An error occurred: {e}"

def generateScript(strlst):
    # RETRIEVE STRINGS FROM LIST ARGUMENT
    sysPrompt_path = strlst[0]
    subprompts_path = strlst[1]
    category = strlst[2]
    videoType = strlst[3]

    sysPrompt_raw = readSysPrompt(sysPrompt_path)
    usrPrompt = f"The video category is: {category}. The video type is: {videoType}."

    subprompts = []
    titles_sps = ['intro','definition','response-to-the-question','conclusion']
    subprompts_raw = parseJSON(subprompts_path)
    for title in titles_sps:
        subprompts.append(subprompts_raw[videoType][title]) 

    sysPrompt = sysPrompt_raw.replace("{sp1}",subprompts[0])
    sysPrompt = sysPrompt.replace("{sp2}",subprompts[1])
    sysPrompt = sysPrompt.replace("{sp3}",subprompts[2])
    sysPrompt = sysPrompt.replace("{sp4}",subprompts[3])

    response = chatbot(sysPrompt,usrPrompt)
    # print(response)

    # PARSE RESPONSE FROM CHATGPT
    chapter_strings = []
    image_prompts = []

    try:
        response_json = json.loads(response)
        for chapter in response_json['chapters']:
            chapter_strings.append(chapter['secondary text'])
            image_prompts.append(chapter['image prompts'])

        # printLog(chapter_strings,image_prompts)

        return chapter_strings,image_prompts
        
    except json.JSONDecodeError as e:
        print(f"JSON decoding failed: {e}")
        exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        exit(1)
