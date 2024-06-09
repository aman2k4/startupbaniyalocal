import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

def read_data(file_path):
    df = pd.read_csv(file_path)
    return df

def preprocess_data(df):
    df['Submit Date (UTC)'] = pd.to_datetime(df['Submit Date (UTC)'])
    df['hour'] = df['Submit Date (UTC)'].dt.hour
    return df

def set_graph_settings():
    font_path = fm.findfont(fm.FontProperties(family='Merriweather Sans', weight='heavy'))
    plt.rcParams['font.family'] = fm.FontProperties(fname=font_path).get_name()
    plt.rcParams['axes.facecolor'] = '#EFEAE4'
    plt.rcParams['lines.color'] = '#380517'

def set_graph_look_and_feel():
    fig, ax = plt.subplots()
    fig.patch.set_facecolor('#EFEAE4')
    ax.set_facecolor('#EFEAE4')

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)

    plt.tick_params(axis='x', colors='#380517')
    plt.tick_params(axis='y', colors='#380517')

def plot_responses_vs_hour(df):
    df_grouped = df.groupby('hour').size().reset_index(name='count')

    set_graph_settings()
    set_graph_look_and_feel()

    plt.scatter(df_grouped['hour'], df_grouped['count'], color='#F55E12')
    plt.xlabel('Hour', color='#380517')
    plt.ylabel('Number of Responses', color='#380517')
    plt.title('Number of Responses vs Hour', color='#380517')
    plt.xticks(range(24))  # Ensure whole number ticks on x-axis
    plt.show()

file_path = 'yam.csv'
df = read_data(file_path)
df = preprocess_data(df)
plot_responses_vs_hour(df)
