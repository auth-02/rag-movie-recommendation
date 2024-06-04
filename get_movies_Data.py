import pandas as pd
import requests
import time
import os

def fetch_movie_data(api_key, movie_ids):
    base_url = 'http://www.omdbapi.com/'
    movie_data = []

    for movie_id in movie_ids:
        response = requests.get(base_url, params={
            'apikey': api_key,
            'i': movie_id,
            'r': 'json',
            'plot': 'full'  
        })
        data = response.json()
        if data.get('Response') == 'True':
            movie_data.append(data)
        else:
            print(f"Error fetching data for movie ID {movie_id}: {data.get('Error')}")
        time.sleep(2) 

    return movie_data

def read_csv(file_path):
    df = pd.read_csv(file_path)
    return df['movie_id'].tolist()

def save_to_csv(data, file_path):
    df = pd.DataFrame(data)
    df.to_csv(file_path, index=False)

api_key = os.getenv("OMDB_API_KEY")
input_csv = 'hindi_data/IMDB-Movie-Dataset(2023-1951).csv'
output_csv = 'hindi_data/scraped_hindi_movie_data.csv'

movie_ids = read_csv(input_csv)

movie_data = fetch_movie_data(api_key, movie_ids)

save_to_csv(movie_data, output_csv)

print(f"Data for {len(movie_data)} movies saved to {output_csv}")
