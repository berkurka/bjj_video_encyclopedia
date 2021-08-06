import os
import sys
import pandas as pd
from datetime import datetime
from numpy import isnan
import streamlit as st

p = os.path.abspath('../..')
if p not in sys.path:
    sys.path.insert(0,p)

# Functions 
def str_time_to_sec(x):
    if x == 0:
        return 0
    pt = datetime.strptime(x,'%H:%M:%S')
    return pt.second + pt.minute*60 + pt.hour*3600


# Load class
@st.cache
def load_data():
    df = pd.read_excel(f'./bjj_videos.xlsx')
    df['tags'] = df['From'] + ', ' + df['To'].fillna('') + ', ' + df['Other'].fillna('')
    df['End_time'] = df['End_time'].fillna(0).apply(str_time_to_sec)
    df['Start_time'] = df['Start_time'].fillna(0).apply(str_time_to_sec)
    return df

st.set_page_config(layout="wide")
df = load_data()
st.title("Brazilian Jiu-Jitsu Instructional Videos")
c1, c2 = st.beta_columns((1, 2))
st.sidebar.header("Search Filters:")


radio = st.sidebar.radio('Language', ['English', 'Portuguese', 'All'])

# Side Pannel---------------------------
if radio == 'All':  
    df_subset = df.copy()
else:
    df_subset = df[df['Language'] == radio]
type_options = list(df_subset['Type'].unique())
pos_type = st.sidebar.selectbox("Select Type", ['All'] + type_options)
if pos_type != 'All':
    df_subset = df_subset[df_subset['Type'] == pos_type]
teacher_options = list(df_subset['Teacher'].unique())
teacher = st.sidebar.selectbox("Select Teacher", ['All'] + teacher_options)
if teacher != 'All':
    df_subset = df_subset[df_subset['Teacher'] == teacher]

title = st.sidebar.text_input('Search using tags', 'Type any tag word')
if title != 'Type any tag word':
    text_matches = df_subset['tags'].str.contains(title).shape[0]
    df_subset = df_subset[df_subset['tags'].str.contains(title)]
else:
    text_matches = 0
df_subset = df_subset.reset_index(drop=True)

# Main page-------------------------------

# c1, c2, c3, c4 = st.beta_columns((2, 1, 1, 1))
with c1:
    st.subheader(f'{df_subset.shape[0]} videos found')
    with st.beta_expander('See all results'):
        st.table(df_subset[['Teacher', 'Type', 'From', 'To']])
    selected_indices = st.multiselect('Select only 1 result:', df_subset.index)
    selected_rows = df_subset.loc[selected_indices]
    st.write('### Selected video:', selected_rows[['Teacher', 'Type', 'From', 'To']].head(1))
with c2:
    if selected_rows.shape[0] > 0:
        url = selected_rows['Link'].iloc[0]
        start_time = selected_rows['Start_time'].iloc[0]
        st.video(url, start_time=start_time)
    else:
        st.write('No row video selected')