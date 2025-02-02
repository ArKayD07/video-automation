from website_apollonian.backend.videogenai.scripts import gen_script, gen_audio, gen_images, gen_video
from datetime import datetime

def gen_test(lst):
    start = datetime.now()
    print("gen_test> Start")
    print("gen_test> Generating scripts...")
    chapter_scripts,img_prompts = gen_script.generateScript(lst)
    print("gen_test> Scripts generated. Generating audio tracks")
    gen_audio.generate_tracks(chapter_scripts)
    print("gen_test> Audio tracks generated. Generating images")
    gen_images.generate_gallery(img_prompts)
    print("gen_test> Images generated.")
    print(f"gen_test> Runtime: {datetime.now() - start}s")


#inpt = ['test_sysPrompt.txt','test_subprompts.json', 'Mental Health', 'informational']
#gen_test(inpt)

inpt = [1,2,6,3]
gen_video.create_video(inpt)