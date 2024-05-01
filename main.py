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

    # Create a single figure to hold all subplots
    from plotly.subplots import make_subplots
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Duration vs Number of Words', 'Duration vs Number of Letters',
                        'Text with Maximum and Minimum Duration', 'Number of Words vs Number of Letters')
    )

    # Duration vs Number of Words
    fig.add_trace(
        go.Scatter(x=durations, y=num_words, mode='markers', text=texts),
        row=1, col=1
    )
    fig.update_xaxes(title_text="Duration", row=1, col=1)
    fig.update_yaxes(title_text="Number of Words", row=1, col=1)

    # Duration vs Number of Letters
    fig.add_trace(
        go.Scatter(x=durations, y=num_letters, mode='markers', text=texts),
        row=1, col=2
    )
    fig.update_xaxes(title_text="Duration", row=1, col=2)
    fig.update_yaxes(title_text="Number of Letters", row=1, col=2)

    # Text with Maximum and Minimum Duration
    max_duration_index = durations.index(max(durations))
    min_duration_index = durations.index(min(durations))
    max_duration_text = texts[max_duration_index]
    min_duration_text = texts[min_duration_index]
    fig.add_trace(
        go.Bar(x=['Max Duration', 'Min Duration'], y=[max(durations), min(durations)], text=[max_duration_text, min_duration_text]),
        row=2, col=1
    )
    fig.update_xaxes(title_text="Duration", row=2, col=1)
    fig.update_yaxes(title_text="Text", row=2, col=1)

    # Number of Words vs Number of Letters
    fig.add_trace(
        go.Scatter(x=num_words, y=num_letters, mode='markers', text=texts),
        row=2, col=2
    )
    fig.update_xaxes(title_text="Number of Words", row=2, col=2)
    fig.update_yaxes(title_text="Number of Letters", row=2, col=2)

    # Update layout for the combined figure
    fig.update_layout(title_text='Subtitle Analysis Charts', height=800, width=1000)
    fig.show()




subtitles = parse_srt('reel15_new.srt')
subtitle_duration = calculate_subtitle_duration(subtitles)
# Call the function to plot charts
plot_charts(subtitle_duration)
save_to_csv(subtitle_duration, 'output.csv')

