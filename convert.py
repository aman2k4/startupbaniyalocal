# create a function which takes in srt file and generate a new one which follows the following rules:
# 1. Keep subtitles atleast 1.5 seconds on the screen. number of words should be in range of 3 to 4 and number of letters should be in range of 10 to 15
# 2. If the sentense end, also end the subtitle at the end of the sentence. and start new sentense with new timestamp
# 3. try to keep the number of words and letters in same range. Maximum 4 words 12 letters is the hard cutoff.
import re
from datetime import timedelta, datetime


def parse_time(time_str):
    hours, minutes, seconds = re.split("[:]", time_str)
    seconds, milliseconds = re.split("[,]", seconds)
    return timedelta(
        hours=int(hours),
        minutes=int(minutes),
        seconds=int(seconds),
        milliseconds=int(milliseconds),
    )


def format_time(delta):
    total_seconds = int(delta.total_seconds())
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    milliseconds = delta.microseconds // 1000
    return f"{hours:02}:{minutes:02}:{seconds:02},{milliseconds:03}"


def process_subtitle(subtitle):
    # this function takes in one subtiltes and process it , such as duration of it, number of letters and number of words etc
    duration = parse_time(subtitle["end_time"]) - parse_time(subtitle["start_time"])
    number_of_words = len(subtitle["text"].split(" "))
    number_of_letters = len(subtitle["text"])

    seconds_per_word = duration.total_seconds() / number_of_words
    seconds_per_letter = duration.total_seconds() / number_of_letters

    print(f"Seconds per word: {seconds_per_word}")
    print(f"Seconds per letter: {seconds_per_letter}")
    return {
        "duration": duration,
        "words": number_of_words,
        "letters": number_of_letters,
        "seconds_per_word": seconds_per_word,
        "seconds_per_letter": seconds_per_letter,
    }


def parse_srt_file(srt_file_path):
    subtitles = []
    with open(srt_file_path, "r", encoding="utf-8") as file:
        content = file.read().split("\n\n")
        for block in content:
            if block.strip():
                lines = block.split("\n")
                index = lines[0]
                times = lines[1]
                text = " ".join(lines[2:])
                start_time, end_time = times.split(" --> ")
                subtitles.append(
                    {"start_time": start_time, "end_time": end_time, "text": text}
                )
    return subtitles


def save_srt_file(output_file_path, new_subtitles):

    with open(output_file_path, "w", encoding="utf-8") as file:
        for index, sub in enumerate(new_subtitles):
            file.write(f"{index + 1}\n")
            file.write(f"{sub['start_time']} --> {sub['end_time']}\n")
            file.write(f"{sub['text']}\n")
            file.write("\n")

def merge_subtitles(subtitles):
    i = 0
    while i < len(subtitles) - 1:
        start_time = parse_time(subtitles[i]["start_time"])
        end_time = parse_time(subtitles[i]["end_time"])
        current_duration = end_time - start_time

        # Print duration in seconds
        print(subtitles[i]["text"])
        print(f"Current duration: {current_duration.total_seconds()} seconds")
        
        if current_duration < timedelta(seconds=1.0):
            subtitles[i]["end_time"] = subtitles[i + 1]["end_time"]
            subtitles[i]["text"] += " " + subtitles[i + 1]["text"]
            del subtitles[i + 1]
        else:
            i += 1
                
    return subtitles

def split_subtitle(subtitles):
    # This function takes in subtitles and splits them if there is a full stop not at the start or end of the text
    new_subtitles = []
    for sub in subtitles:
        if "." in sub["text"] and sub["text"].index(".") != len(sub["text"]) - 1:
            parts = sub["text"].split(".")
            parts = [part.strip() + '.' for part in parts if part.strip()]
            if parts[-1][-1] != '.':
                parts[-1] = parts[-1][:-1]  # Remove the dot added to the last part if it originally didn't end with a dot
            
            start_time = parse_time(sub["start_time"])
            end_time = parse_time(sub["end_time"])
            total_duration = (end_time - start_time).total_seconds()
            
            # Calculate duration based on number of characters
            total_chars = sum(len(part) for part in parts)
            char_time = total_duration / total_chars
            
            current_start_time = start_time
            for i, part in enumerate(parts):
                part_duration = len(part) * char_time
                part_end_time = current_start_time + timedelta(seconds=part_duration)
                
                # Adjust the start time of the next part
                if i < len(parts) - 1:
                    next_start_time = part_end_time + timedelta(milliseconds=50)
                else:
                    next_start_time = part_end_time
                
                new_subtitles.append({
                    "start_time": format_time(current_start_time),
                    "end_time": format_time(part_end_time),
                    "text": part
                })
                
                current_start_time = next_start_time
        else:
            new_subtitles.append(sub)  # Add the subtitle as is if no splitting is needed

    return new_subtitles


def create_new_srt_file(srt_file_path, output_file_path):

    subtitles = parse_srt_file(srt_file_path)

    subtitles = merge_subtitles(subtitles)
    # Save new subtitles to output file
    save_srt_file('01_'+ output_file_path, subtitles)
    # Split the subtitles if there is full stop
    subtitles = split_subtitle(subtitles)

    # Save new subtitles to output file
    save_srt_file(output_file_path, subtitles)


create_new_srt_file("reel15.srt", "reel15_new.srt")
