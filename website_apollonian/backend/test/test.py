from website_apollonian.backend.videogenai.scripts import gen_script,gen_audio

lst = ['test_sysPrompt.txt','test_subprompts.json', 'Mental Health', 'informational']
chapter_scripts,img_prompts = gen_script.generateScript(lst)
gen_audio.generate_tracks(chapter_scripts)