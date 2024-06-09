from moviepy.editor import *

def create_background():
    # Create a white background
    background = ColorClip((1080, 1920), color=(255, 255, 255), duration=3)
    return background

def create_text_clips(background, fontsize=25, font='manrope', stroke_width=5):
    # Generate the video with the word "AI" continuously added
    text_width, text_height = TextClip("AI ", fontsize=fontsize, font=font).size
    cols = background.size[0] // text_width
    rows = background.size[1] // text_height

    # Pre-create the text clip to avoid redundant creation
    text_clip_template = TextClip("AI", fontsize=fontsize, color='black', font=font, stroke_width=stroke_width).set_duration(background.duration)
    # Set font and font weight
    text_clip_template = text_clip_template.set_opacity(1)

    col = 0
    row = 0
    text_clips = []

    for i in range(rows * cols):
        pos = (col * text_width, row * text_height)
        # Slow down the appearance of each text clip by increasing the start time interval
        start_second = i * (background.duration / (rows * cols))
        text_clips.append(text_clip_template.set_pos(pos).set_start(start_second))
        col += 1
        if col >= cols:
            col = 0
            row += 1

    return text_clips

def create_final_clip(background, text_clips):
    final_clip = CompositeVideoClip([background] + text_clips)
    return final_clip

def write_video(final_clip, output_file, fps=30, threads=1, codec="libx264"):
    # Write the video to a file using a different codec
    final_clip.write_videofile(output_file, fps=fps, threads=threads, codec=codec)

background = create_background()
write_video(background, "background.mp4")
text_clips = create_text_clips(background)
final_clip = create_final_clip(background, text_clips)
write_video(final_clip, "ai_video2.mp4")
