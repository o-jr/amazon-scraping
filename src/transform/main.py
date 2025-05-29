
import pandas as pd
import sqlite3
import datetime
import os


print("Current Working Directory:", os.getcwd()) # Print current working directory
file_path = '../ml-scraping/data/data3.json' # Define file path
print("Looking for file at:", os.path.abspath(file_path)) # Print absolute path for debugging

df = pd.read_json(file_path)

# Set the display options to show all columns
df['Source'] = 'amzn/oculos-masculino'
df['Created_at'] = datetime.datetime.now() #.strftime('%Y-%m-%d %H:%M:%S')
df = df[df['brand'].notnull() & df['price'].notnull()]
df['brand'] = df['brand'].replace({'Generic': 'Genérico', 'ROCK BROS': 'ROCKBROS'})
df['price'] = df['price'].fillna(0).astype(float)
df['rating'] = df['rating'].fillna(0).astype(float)
#df['page'] = df['page'].fillna(1).astype(int)  # Ensure 'page' is an integer
df['page'] > 0
df['title'] = df['title'].str.strip()  # Remove leading/trailing whitespace from titles

conn = sqlite3.connect('../ml-scraping/data/amazon.db')
df.to_sql('ml_items', conn, if_exists='append', index=False)
conn.close()

#print(df.head())
print("Data saved to SQLite database.")


