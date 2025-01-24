import openai
import edge_tts
import asyncio

openai.api_key = "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"

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
        asyncio.run(communicate.save(audio_name))
    except Exception as e:
        print(f"An error occurred: {e}")

question = input('Enter a question: ')
response = chatbot(prompt)

chapters = response.split("\n\n")
chapter_strings = []
for chapter in chapters:
    chapter_strings.append(chapter.replace(chapter[chapter.find('*'):chapter.find('\n')], "").replace('\n', ''))

for i in range(len(chapter_strings)):
    audio_name = 'audio-' + str(i+1) + ".mp3"
    generate_audio(chapter_strings[i],audio_name)
