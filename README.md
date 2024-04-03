YOUTUBE DATA HARVESTING AND WAREHOUSING USING SQL AND STREAMLIT

This project demonstrates a workflow for harvesting data from YouTube channels, storing it in a SQL database, and visualizing the data using a Streamlit web application.

OVERVIEW

YouTube is a rich source of data, including information about channels, videos, views, likes, comments, and more. This project aims to harvest data from YouTube channels, store it in a MySQL database, and provide an interactive interface for querying and visualizing the data using STREAMLIT web application.

COMPONENTS

 	YouTube Data Retrieval: Utilizes the YouTube Data API to fetch channel and video details such as titles, views, likes, comments, and other relevant metrics.

 	MySQL Database: Stores the harvested YouTube data in a relational database management system (MySQL). Separate tables are used to store information about channels details and video details.

 	Streamlit Web Application: Provides a user-friendly interface for querying the YouTube data stored in the MySQL database. Users can input a YouTube channel ID, retrieve channel details, fetch video details, execute SQL queries.

SETUP

API Key: Obtain an API key from the YouTube Data API and replace the api_key variable in the code with your own API key.
To create an API key for the YouTube Data API, you'll need to follow these steps:
a.	Go to the Google Developers Console: Visit the Google Developers Console website and sign in with your Google account.
b.	Create a new project: If you don't have an existing project, create a new one by clicking on the "Select a project" dropdown menu at the top of the page and then clicking on the "New Project" button. Follow the prompts to create the project.
c.	Enable the YouTube Data API: Once you've created a project (or selected an existing one), navigate to the "APIs & Services" > "Library" page using the menu on the left. Search for "YouTube Data API" and click on it. Then click the "Enable" button to enable the API for your project.
d.	Enable the YouTube Data API: Once you've created a project (or selected an existing one), navigate to the "APIs & Services" > "Library" page using the menu on the left. Search for "YouTube Data API" and click on it. Then click the "Enable" button to enable the API for your project.
e.	Copy API key: Once your API key is generated, copy it and securely store it. You'll need to use this key in your application to authenticate with the YouTube Data API.
f.	Usage: Use the API key in your application by including it in the API requests to authenticate and access the YouTube Data API.


MySQL Database: Set up a MySQL database and configure the connection parameters (host, username, password, database name) in the code.
mydb = pymysql.connect( 
host = 'localhost' ,
user = 'root'   ,
password = ********', 
database = '******'  
)

Python Libraries: Install the Python libraries like pandas , googleapiclient, streamlit, pymysql using pip:
Pip install pandas
Pip install googleapiclient.discovery
Pip install streamlit
Pip install pymysql

Usage
Retrieve Channel Details: Enter a YouTube channel ID in the Streamlit interface to fetch and display details about the channel, including name, subscribers, and total video count.

Retrieve Video Details: After entering a channel ID, use the provided button to fetch and display details about the channel's videos, including titles, views, likes, comments, and other metrics.

Execute SQL Queries: Choose from a list of predefined SQL queries or input custom queries. The results will be displayed in tabular format.

