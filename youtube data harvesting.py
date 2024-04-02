
import pymysql
import pandas as pd
import streamlit as st
from googleapiclient.discovery import build

# Define API key
api_key = "AIzaSyDhpNofdxhQBVsRiU4GKv497kjU16labms"

# Function to retrieve channel details
def get_channel_details(channel_id):
    youtube = build('youtube', 'v3', developerKey=api_key)

    # Retrieve channel details
    request = youtube.channels().list(
        part="snippet,statistics",
        id=channel_id
    )
    response = request.execute()

    # Extract relevant information
    channel_info = {
        "Channel Name": response['items'][0]['snippet']['title'],
        "channel id": channel_id,
        "Subscribers": response['items'][0]['statistics'].get('subscriberCount', 0),
        "Total Video Count": response['items'][0]['statistics'].get('videoCount', 0)
    }
    return channel_info

def get_all_video_details(channel_id):
    youtube = build('youtube', 'v3', developerKey=api_key)

    video_details = []

    next_page_token = None

    while True:
        # Retrieve videos from channel
        request = youtube.search().list(
            part="snippet",
            channelId=channel_id,
            maxResults=50,  # Adjust this value as needed
            pageToken=next_page_token
        )
        response = request.execute()

        # Extract video details
        for item in response['items']:
            if 'id' in item and 'videoId' in item['id']:
                video_id = item['id']['videoId']
                video_detail = get_single_video_details(youtube, video_id)
                video_details.append(video_detail)

        # Check if there are more pages
        if 'nextPageToken' in response:
            next_page_token = response['nextPageToken']
        else:
            break

    return video_details

def get_single_video_details(youtube, video_id):
    # Retrieve details for a single video
    request = youtube.videos().list(
        part="snippet,statistics, contentDetails",
        id=video_id
    )
    response = request.execute()
    duration = response['items'][0]['contentDetails']['duration']
    duration_seconds = convert_duration_to_seconds(duration)
    video_detail = {
        "Video Title": response['items'][0]['snippet']['title'],
        "Video ID": video_id,
        "published_year": response['items'][0]['snippet']['publishedAt'][:4],
        "Likes": response['items'][0]['statistics'].get('likeCount', 0),
        "Dislikes": response['items'][0]['statistics'].get('dislikeCount', 0),
        "Comments": response['items'][0]['statistics'].get('commentCount', 0),
        "views": response['items'][0]['statistics'].get('viewCount', 0),
        "duration_secs": duration_seconds
        
    }

    return video_detail
# Function to convert duration to seconds
def convert_duration_to_seconds(duration):
    total_seconds = 0
    if duration.startswith('PT'):
        time_str = duration[2:]  # Extract time part
        hours, minutes, seconds = 0, 0, 0

    # Parse time string
        if 'H' in time_str:
            hours = int(time_str.split('H')[0])
            time_str = time_str.split('H')[1]
        if 'M' in time_str:
            if 'H' not in time_str:  # Check if minutes are specified without hours
                minutes = int(time_str.split('M')[0])
                time_str = time_str.split('M')[1]
            else:
                minutes = int(time_str.split('M')[0])
                time_str = time_str.split('M')[1]
        if 'S' in time_str:
            seconds = int(time_str.split('S')[0])


        # Calculate total duration in seconds
        total_seconds = hours * 3600 + minutes * 60 + seconds

    return total_seconds

# Connect to MySQL
def connect_to_mysql():
    # MySQL connection parameters
    host = 'localhost'  # or your MySQL server IP address
    user = 'root'   # your MySQL username
    password = '1qaz@WSX3edc'  # your MySQL password
    database = 'ytdb'  # your MySQL database name

    # Connect to MySQL
    return pymysql.connect(host=host, user=user, password=password, database=database)

# Function to save channel details to MySQL
def save_channel_details_to_mysql(channel_info, conn):
    cur = conn.cursor()
    
    cur.execute("""
        INSERT INTO channel_details (channel_name, subscribers, total_video_count)
        VALUES (%s, %s, %s)
    """, (channel_info['Channel Name'], channel_info['Subscribers'], channel_info['Total Video Count']))
    conn.commit()
    cur.close()

# Function to save video details to MySQL
def save_video_details_to_mysql(video_details, conn, channel_info):
    cur = conn.cursor()
    for video_detail in video_details:
        cur.execute("""
            INSERT INTO video_details (channel_name, channel_id, video_title, video_id, likes, dislikes, comments,view_count,YEAR,video_duration_secs)
            VALUES (%s, %s, %s, %s, %s, %s, %s,%s,%s,%s)
        """, (channel_info['Channel Name'], channel_info['channel id'], video_detail['Video Title'], 
              video_detail['Video ID'], video_detail['Likes'], video_detail['Dislikes'], video_detail['Comments'],video_detail['views'],video_detail['published_year'],video_detail['duration_secs']))
    conn.commit()
    cur.close()

# Function to execute SQL query and fetch results
def display_sql_query_results(conn, sql_query, query_description):
    # Create cursor
    cursor = conn.cursor()

    # Execute SQL query and fetch results
    cursor.execute(sql_query)
    results = cursor.fetchall()

    # Close cursor
    cursor.close()

    # Display results
    st.subheader(query_description)
    if results:
        df = pd.DataFrame(results, columns=[desc[0] for desc in cursor.description])
        st.dataframe(df)
    else:
        st.write("No results found for this query.") 


# Execute SQL query to retrieve channel details
def get_channel_details_from_mysql():
    conn = connect_to_mysql()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM channel_details")
    # Fetch all rows
    channel_details = cursor.fetchall()

    # Close cursor and connection
    cursor.close()
    conn.close()
    return channel_details

 # Execute SQL query to retrieve video details
def get_video_details_from_mysql():
    conn = connect_to_mysql()
    cursor = conn.cursor()
 
    cursor.execute("SELECT * FROM video_details")

    # Fetch all rows
    video_details = cursor.fetchall()

    # Close cursor and connection
    cursor.close()
    conn.close()

    return video_details


def main():
    # Create tabs in the sidebar
    tab = st.sidebar.radio("Navigation", ["Home", "Query Results","Table List"])
    if tab == "Home":
        st.title("YouTube Data Harvesting and Warehousing using SQL and Streamlit")
    # Input for YouTube channel ID
        channel_id = st.text_input("Enter YouTube Channel ID:")
        if channel_id:
            st.write("Channel ID entered:", channel_id)
        
            # Retrieve and display channel details
            channel_info = get_channel_details(channel_id)
            st.subheader("Channel Details")
            st.write(pd.json_normalize(channel_info))

         # Button to retrieve and store video details
            if st.button("Retrieve and Store Video Details"):
                st.write("Fetching video details...")
                video_details = get_all_video_details(channel_id)
                st.subheader("Video Details")
                st.write(pd.json_normalize(video_details))

                # Connect to MySQL
                conn = connect_to_mysql()

                # Save channel details to MySQL
                save_channel_details_to_mysql(channel_info, conn)

                # Save video details to MySQL
                save_video_details_to_mysql(video_details, conn, channel_info)

                # Close MySQL connection
                conn.close()

       
        

    elif tab == "Query Results":
        st.title("Query Results")
        # Connect to MySQL
        conn = connect_to_mysql()
        
        selected_option = st.selectbox("Select an option", ["What are the names of all the videos and their corresponding channels?", "Which channels have the most number of videos, and how many videos do they have?","What are the top 10 most viewed videos and their respective channels?","How many comments were made on each video, and what are their corresponding video names?","Which videos have the highest number of likes, and what are their corresponding channel names?","What is the total number of likes and dislikes for each video, and what are their corresponding video names?","What is the total number of views for each channel, and what are their corresponding channel names?","What are the names of all the channels that have published videos in the year 2022?","What is the average duration of all videos in each channel, and what are their corresponding channel names?","Which videos have the highest number of comments, and what are their corresponding channel names?"])
        st.write("You selected:", selected_option)
        queries = {
            "What are the names of all the videos and their corresponding channels?": "SELECT channel_name,video_title from video_details",
            "Which channels have the most number of videos, and how many videos do they have?": """
        SELECT channel_name, COUNT(video_id) AS video_count FROM video_details
        GROUP BY channel_name
        ORDER BY video_count DESC
        LIMIT 1;""",
            "What are the top 10 most viewed videos and their respective channels?": """
        SELECT channel_name,video_title, view_count FROM video_details
        ORDER BY view_count DESC
        LIMIT 10;""",
            "How many comments were made on each video, and what are their corresponding video names?":"SELECT video_title,comments FROM video_details",
            "Which videos have the highest number of likes, and what are their corresponding channel names?":"""SELECT channel_name,video_title,likes FROM video_details
            ORDER BY likes DESC""",
            "What is the total number of likes and dislikes for each video, and what are their corresponding video names?":"""SELECT video_title,
               SUM(likes) AS total_likes,
               SUM(dislikes) AS total_dislikes FROM video_details
        GROUP BY video_title;""",
            "What is the total number of views for each channel, and what are their corresponding channel names?":"""SELECT channel_name,SUM(view_count) AS views FROM video_details
            GROUP BY channel_name;""",
            "What are the names of all the channels that have published videos in the year 2022?":"""SELECT DISTINCT channel_name,YEAR FROM video_details WHERE YEAR = 2022;""",
            "What is the average duration of all videos in each channel, and what are their corresponding channel names?":"""SELECT channel_name, AVG(video_duration_secs) AS avg_duration FROM video_details GROUP BY channel_name;""",
            "Which videos have the highest number of comments, and what are their corresponding channel names?": """SELECT channel_name,video_title,comments FROM video_details
            ORDER BY comments DESC;"""
        }    
        sql_query = queries[selected_option]
        display_sql_query_results(conn, sql_query, f"Results for {selected_option}")
            
        conn.close()
    elif tab == "Table List":
        st.title("TABLES LIST")
        
        st.subheader("channel_details")
        channel_details=get_channel_details_from_mysql()
        st.write(pd.DataFrame(channel_details,columns=["Channel_Name", "Subscribers", "Total_Video_Count"]))
        
        st.subheader("video_details")
        video_details = get_video_details_from_mysql()
        st.write(pd.DataFrame(video_details,columns=["Channel_Name", "channel_id", "video_title","video_id","likes","dislikes","comments","view_count","published_year","video_duration_secs"]))
        
                
if __name__ == "__main__":
    main()


