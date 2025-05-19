# Vamos importar o que precisamos
import pandas as pd
import sqlite3
import datetime
import os


print("Current Working Directory:", os.getcwd()) # Print current working directory

file_path = '../ml-scraping/data/data.json' # Define file path

print("Looking for file at:", os.path.abspath(file_path)) # Print absolute path for debugging

df = pd.read_json(file_path)

# Set the display options to show all columns
#pd.options.display.max_columns = None

df['Source'] = 'ml/oculos-masculino'
df['Created_at'] = datetime.datetime.now() #.strftime('%Y-%m-%d %H:%M:%S')

df['brand'] = df['brand'].str.replace('Brand: ', '', regex=False)
df['price'] = df['price'].fillna(0).astype(float)
df['rating'] = df['rating'].fillna(0).astype(float)





conn = sqlite3.connect('../ml-scraping/data/database.db')
df.to_sql('ml_items', conn, if_exists='replace', index=False)
conn.close()

#print(df.head())
print("Data saved to SQLite database.")