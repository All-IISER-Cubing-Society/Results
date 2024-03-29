import os

import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image

favicon = Image.open("media/favicon.ico")
st.set_page_config(
    page_title = "AICS Results",
    page_icon = favicon,
    menu_items={
         'Get Help': 'https://github.com/All-IISER-Cubing-Society/Results',
         'Report a bug': "https://github.com/All-IISER-Cubing-Society/Results/issues",
         'About': "AICS Results is a Streamlit app to visualize data of weekly event results. Contact Purva at AICS for any issues or help."
     }
)

results = "results/"

@st.cache
def load_data():
    # Get all files in the results directory
    files = os.listdir("results")
    frames = []
    
    # Loop through all files and append dataframes to a list
    for f in files:
        df = pd.read_csv(os.path.join("results", f))
        
        # Convert Date column to datetime field
        df['Date'] = pd.to_datetime(df['Date'])
        
        # Create an event column
        event = f.rstrip(".csv")
        df['Event'] = [event for i in range(len(df))]

        # Append to list
        frames.append(df)

    # Create combined data frame
    cdf = pd.concat(frames)
    
    return cdf


@st.cache
def load_event_data(data, events):
    frames = []
    for event in events:
        df = data[data['Event'] == event]
        frames.append(df)
    
    combined_data = pd.concat(frames)
    
    return combined_data

cdf = load_data()

st.sidebar.title("AICS - Results")

category = st.sidebar.radio(
    'Select Category',
    ('Individual Results', 'Best Results', 'Institute-wise Results', 'Institute Leaderboard'))


if category == 'Individual Results':

    # Get list of names in sorted order
    names = sorted(cdf['Name'].unique())

    # Sidebar name selector
    name = st.sidebar.selectbox('Name', names)

    # Person specific data
    df = cdf[cdf['Name'] == name]
    institute = df['Institute'].iloc[0]

    st.header(name)
    st.subheader(institute)

    # Get events
    events = df['Event'].unique()

    selected_events = st.multiselect('Events', events, '3x3')

    if len(selected_events) > 0:
        selected_events_df = load_event_data(df, selected_events)
        st.write("The graph is interactive. Feel free to play around with it.")
        if 'FMC' in selected_events and len(selected_events) > 1:
            st.write("FMC results are in Moves, and others in seconds. It would be better to plot FMC as a single graph.")
        fig = px.line(selected_events_df, x='Date', y='Result', color='Event', markers=True)

        st.plotly_chart(fig, use_container_width=True)
    else:
        st.write("Please select some events.")

    st.write("If on mobile, select name from sidebar on top left.")

    st.header("Event Participation")
    participation_df = df['Event'].value_counts().reset_index()
    participation_df.columns = ['Event', 'Count']
    participation_df = participation_df.sort_values('Count', ascending=False)
    st.dataframe(participation_df)

elif category == 'Best Results':
    events = sorted(cdf['Event'].unique())
    
    event = st.sidebar.selectbox('Event', events)
    
    df = cdf[cdf['Event'] == event]
    
    # First sort by Result, then do a stable sort on Name
    df = df.sort_values('Result').sort_values('Name', kind='stable')
    
    # Drop duplicates, then sort by result again
    df = df.loc[df['Name'] != df['Name'].shift()].sort_values('Result')
    
    df['Result'] = df['Result'].astype(str)
    df['Date'] = df['Date'].astype(str)
    df = df.reset_index().drop(columns=['index', 'Event'])
    
    st.header(event)
    st.write(df)

elif category == "Institute-wise Results":
    institutes = sorted(cdf['Institute'].unique())
    
    institute = st.sidebar.selectbox('Institute', institutes)
    idf = cdf[cdf['Institute'] == institute]
    
    st.header("Institute-wise Results")
    st.subheader(institute)
    
    events = sorted(idf['Event'].unique())
    
    event = st.selectbox('Eevnt', events)
    
    df = idf[idf['Event'] == event]
    
    # First sort by Result, then do a stable sort on Name
    df = df.sort_values('Result').sort_values('Name', kind='stable')
    
    # Drop duplicates, then sort by result again
    df = df.loc[df['Name'] != df['Name'].shift()].sort_values('Result')
    
    df['Result'] = df['Result'].astype(str)
    df['Date'] = df['Date'].astype(str)
    df = df.reset_index().drop(columns=['index', 'Event'])
    
    st.write(df)

elif category == "Institute Leaderboard":
    events = sorted(cdf['Event'].unique())
    
    event = st.sidebar.selectbox('Event', events)
    
    df = cdf[cdf['Event'] == event]
    
    # First sort by Result, then do a stable sort on Institute
    df = df.sort_values('Result').sort_values('Institute', kind='stable')
    
    # Drop duplicates, then sort by result again
    df = df.loc[df['Institute'] != df['Institute'].shift()].sort_values('Result')
    
    df['Result'] = df['Result'].astype(str)
    df['Date'] = df['Date'].astype(str)
    df = df.reset_index().drop(columns=['index', 'Event'])
    
    st.header("Institute Leaderboard")
    st.subheader(event)
    st.write(df)
    
image = Image.open("media/AICS-Logo-Dark.png")
st.sidebar.image(image)
st.sidebar.markdown("[Website](https://all-iiser-cubing-society.github.io/#/) | [Instagram](https://www.instagram.com/all.iiser.cubing.society/) | [YouTube](https://www.youtube.com/channel/UCXOIh4FS48Dwy3BC9_FhprA)")
