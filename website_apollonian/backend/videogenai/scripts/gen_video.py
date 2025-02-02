from moviepy import ImageClip, AudioFileClip, VideoFileClip, concatenate_videoclips

def fetch_images(numlst):
    chapters = ['intro','definition','qresponse','conclusion']
    image_clips = []
    for i in range(len(chapters)):
        image_clips_entry = []
        for j in range(numlst[i]):
            image_clips_entry.append(ImageClip(f"tmp/images/{chapters[i]}-{j+1}.png"))
        image_clips.append(image_clips_entry)
    
    return image_clips

def audio_clips():
    chapters = ['intro','definition','qresponse','conclusion']
    audio_clips = []
    for i in range(len(chapters)):
        audio_clips.append(AudioFileClip(f"tmp/audio/audio-{i+1}.mp3"))
    
    return audio_clips

def chapter_clips(chaudio, chimages, chtitle):
    audio_duration = chaudio.duration
    img_num = len(chimages)
    img_duration = audio_duration / img_num

    img_clips = []
    for imgclip in chimages:
        img_clips.append(imgclip.with_duration(img_duration))
    
    chapter_clip = concatenate_videoclips(img_clips, method='compose')
    chapter_clip.audio = chaudio

    chapter_clip.write_videofile(f'tmp/videos/video-{chtitle}.mp4',fps=30)

    return 0

def create_video(lst):
    print(f"gen_video> Start")
    chapters = ['intro','definition','qresponse','conclusion']
    print("gen_video> Retrieving audio clips...")
    audioscl = audio_clips()
    print(f"gen_video> {len(audioscl)} audio clips retrieved. Retrieving image clips...")
    imagescl = fetch_images(lst)
    print(f"gen_video> {len(imagescl)} video clips retrieved. Creating chapter clips...")
    chapterscl = []
    for i in range(len(audioscl)):
        chapter_clips(audioscl[i],imagescl[i],chapters[i])
        chapterscl.append(VideoFileClip(f'tmp/videos/video-{chapters[i]}.mp4'))
    
    print(f"gen_video> Stitching {len(chapterscl)} together...")
    final_video = concatenate_videoclips(chapterscl)
    print(f"gen_video> Writing video file...")
    final_video.write_videofile(f'tmp/videos/final-video.mp4', fps=30)
    print(f"gen_video> Finished!")
    return 0



    
