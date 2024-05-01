import csv
import plotly.graph_objects as go

def parse_srt(file_path):
    subtitles = []
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        index = 0
        while index < len(lines):
            if lines[index].strip().isdigit():
                index += 1
                timing = lines[index].strip().split(' --> ')
                start_time = timing[0]
                end_time = timing[1]
                index += 1
                subtitle_text = ''
                while index < len(lines) and lines[index].strip() != '':
                    subtitle_text += lines[index].strip() + ' '
                    index += 1
                subtitles.append({'start_time': start_time, 'end_time': end_time, 'text': subtitle_text.strip()})
            else:
                index += 1
    return subtitles

def calculate_subtitle_duration(subtitles):
    subtitle_duration = []
    for subtitle in subtitles:
        start_time_parts = subtitle['start_time'].split(':')
        end_time_parts = subtitle['end_time'].split(':')
        start_seconds = int(start_time_parts[0]) * 3600 + int(start_time_parts[1]) * 60 + float(start_time_parts[2].replace(',', '.'))
        end_seconds = int(end_time_parts[0]) * 3600 + int(end_time_parts[1]) * 60 + float(end_time_parts[2].replace(',', '.'))
        duration = end_seconds - start_seconds
        num_letters = len(subtitle['text'].replace(' ', ''))
        num_words = len(subtitle['text'].split())
        subtitle_duration.append({'duration': duration, 'text': subtitle['text'], 'num_letters': num_letters, 'num_words': num_words})
    return subtitle_duration

def save_to_csv(subtitle_duration, output_file):
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['duration', 'text', 'num_letters', 'num_words']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for subtitle in subtitle_duration:
            writer.writerow(subtitle)



def plot_charts(subtitle_duration):
    # Extracting data for plotting
    durations = [sub['duration'] for sub in subtitle_duration]
    num_words = [sub['num_words'] for sub in subtitle_duration]
    num_letters = [sub['num_letters'] for sub in subtitle_duration]
    texts = [sub['text'] for sub in subtitle_duration]

    # Duration vs Number of Words
    fig1 = go.Figure(data=go.Scatter(x=durations, y=num_words, mode='markers', text=texts))
    fig1.update_layout(title='Duration vs Number of Words', xaxis_title='Duration (s)', yaxis_title='Number of Words')
    fig1.show()

    # Duration vs Number of Letters
    fig2 = go.Figure(data=go.Scatter(x=durations, y=num_letters, mode='markers', text=texts))
    fig2.update_layout(title='Duration vs Number of Letters', xaxis_title='Duration (s)', yaxis_title='Number of Letters')
    fig2.show()

    # Text with Maximum and Minimum Duration
    max_duration_index = durations.index(max(durations))
    min_duration_index = durations.index(min(durations))
    max_duration_text = texts[max_duration_index]
    min_duration_text = texts[min_duration_index]
    fig3 = go.Figure(data=[go.Bar(x=['Max Duration', 'Min Duration'], y=[max(durations), min(durations)], text=[max_duration_text, min_duration_text]))
    fig3.update_layout(title='Text with Maximum and Minimum Duration', xaxis_title='Type', yaxis_title='Duration (s)')
    fig3.show()

    # Number of Words vs Number of Letters
    fig4 = go.Figure(data=go.Scatter(x=num_words, y=num_letters, mode='markers', text=texts))
    fig4.update_layout(title='Number of Words vs Number of Letters', xaxis_title='Number of Words', yaxis_title='Number of Letters')
    fig4.show()

# Call the function to plot charts
plot_charts(subtitle_duration)

# Replace 'your_srt_file.srt' with the path to your SRT file
# Replace 'output.csv' with the desired output CSV file path
subtitles = parse_srt('reel15.srt')
subtitle_duration = calculate_subtitle_duration(subtitles)
save_to_csv(subtitle_duration, 'output.csv')
