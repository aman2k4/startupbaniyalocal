
# create a function which takes in srt file and generate a new one which follows the following rules: 
# 1. Keep subtitles atleast 1.5 seconds on the screen. number of words should be in range of 3 to 4 and number of letters should be in range of 10 to 15 
# 2. If the sentense end, also end the subtitle at the end of the sentence. and start new sentense with new timestamp 
# 3. try to keep the number of words and letters in same range. Maximum 4 words 12 letters is the hard cutoff.
import re
from datetime import timedelta, datetime

def parse_time(time_str):
    hours, minutes, seconds = re.split('[:]', time_str)
    seconds, milliseconds = re.split('[,]', seconds)
    return timedelta(hours=int(hours), minutes=int(minutes), seconds=int(seconds), milliseconds=int(milliseconds))

def format_time(delta):
    total_seconds = int(delta.total_seconds())
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    milliseconds = delta.microseconds // 1000
    return f"{hours:02}:{minutes:02}:{seconds:02},{milliseconds:03}"

def parse_srt_file(srt_file_path):
    subtitles = []
    with open(srt_file_path, 'r', encoding='utf-8') as file:
        content = file.read().split('\n\n')
        for block in content:
            if block.strip():
                lines = block.split('\n')
                index = lines[0]
                times = lines[1]
                text = ' '.join(lines[2:])
                start_time, end_time = times.split(' --> ')
                subtitles.append({'start_time': start_time, 'end_time': end_time, 'text': text})
    return subtitles


def save_srt_file(output_file_path, new_subtitles):
    
    with open(output_file_path, 'w', encoding='utf-8') as file:
        for index, sub in enumerate(new_subtitles):
            file.write(f"{index + 1}\n")
            file.write(f"{sub['start_time']} --> {sub['end_time']}\n")
            file.write(f"{sub['text']}\n")
            file.write("\n")


def create_new_srt_file(srt_file_path, output_file_path):
    new_subtitles = []
    last_end_time = None
    subtitles = parse_srt_file(srt_file_path)

    for i, sub in enumerate(subtitles):
        start_time = parse_time(sub['start_time'])
        end_time = parse_time(sub['end_time'])

        # Adjust start time if it overlaps with the last subtitle's end time
        if last_end_time and start_time <= last_end_time:
            start_time = last_end_time + timedelta(milliseconds=10)  # Adding a small delay

        # # Ensure minimum duration of 1.2 seconds, adjust if necessary
        # min_duration = timedelta(seconds=1.2)
        # while (end_time - start_time) < min_duration:
        #     if min_duration > timedelta(seconds=1.0):
        #         min_duration -= timedelta(seconds=0.05)
        #     else:
        #         break
        #     end_time = start_time + min_duration

        # Merge current subtitle with next one if its duration is below 1 second
        current_duration = end_time - start_time
        if current_duration < timedelta(seconds=1.0):
            print(f"Merging subtitle {i} with next one")
            if i < len(subtitles) - 1:
                end_time = parse_time(subtitles[i + 1]['end_time'])
                sub['text'] += ' ' + subtitles[i + 1]['text']
                subtitles.pop(i + 1)  # Remove the next subtitle as it is merged with the current one


        new_subtitles.append({'start_time': format_time(start_time), 'end_time': format_time(end_time), 'text': sub['text']})

        last_end_time = end_time

    # Save new subtitles to output file
    save_srt_file(output_file_path, new_subtitles)




create_new_srt_file('reel15.srt', 'reel15_new.srt')