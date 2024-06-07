from moviepy.editor import *
import sys

# Create a white background
background = ColorClip((1080, 1920), color=(255, 255, 255), duration=3)

# Generate the video with the word "AI" continuously added
fontsize = 25
text_width, text_height = TextClip("AI ", fontsize=fontsize, font='manrope').size
cols = background.size[0] // text_width
rows = background.size[1] // text_height

# Pre-create the text clip to avoid redundant creation
text_clip_template = TextClip("AI", fontsize=fontsize, color='black', font='manrope', stroke_width=5).set_duration(background.duration)
# Set font and font weight
text_clip_template = text_clip_template.set_opacity(1)

col = 0
row = 0
text_clips = []
print(rows )
print(cols)
print(background.duration)

# sys.exit()

for i in range(rows * cols):
    pos = (col * text_width, row * text_height)
    # Slow down the appearance of each text clip by increasing the start time interval
    start_second = i * (background.duration / (rows * cols))
    # print(start_second)
    text_clips.append(text_clip_template.set_pos(pos).set_start(start_second))
    col += 1
    if col >= cols:
        col = 0
        row += 1

final_clip = CompositeVideoClip([background] + text_clips)

# Write the video to a file using a different codec
final_clip.write_videofile("ai_video2.mp4", fps=30, threads=1, codec ="libx264")
