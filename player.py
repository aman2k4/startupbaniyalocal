import moviepy.editor as mpy
from moviepy.video.tools.subtitles import SubtitlesClip

def add_subtitles_to_video(video_path, subtitle_path, output_path):
    # Load the video file
    video = mpy.VideoFileClip(video_path)

    # Create a function to generate text clips for subtitles
    def generator(txt):
        return mpy.TextClip(
            txt, font="Arial", fontsize=20, color="white", bg_color="black"
        )

    # Load the subtitles
    subtitles = SubtitlesClip(subtitle_path, generator)

    # Set the position of the subtitles in the middle of the video
    subtitles = subtitles.set_position(("center", "center"))

    # Overlay the subtitles on the video
    final_video = mpy.CompositeVideoClip([video, subtitles])

    # Write the result to a file
    final_video.write_videofile(output_path, codec="libx264")


# Example usage
add_subtitles_to_video("reel15.mp4", "reel15_new.srt", "output_video.mp4")
