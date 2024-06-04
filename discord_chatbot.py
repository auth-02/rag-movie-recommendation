import os
import discord
from discord.ext import commands
from discord.ui import Button, View
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

# Sample data
recommendations = [
    {
        "Title": "Rocky Aur Rani Kii Prem Kahaani",
        "Plot": "A sensual love story...",
        "Runtime": "168 min",
        "Release Year": 2023,
        "Actor": "Ranveer Singh, Alia Bhatt, Dharmendra",
        "Director": "Karan Johar",
        "Website": "https://www.primevideo.com/detail/Rocky-Aur-Rani-Kii-Prem-Kahaani/0I6U0N56BVTVGY24EM2FARBNIC",
        "Poster": "https://m.media-amazon.com/images/M/MV5BNzAyOWQ4MjUtMGNkMi00ODBkLWEyZDgtY2Q0YjJhYjg3MzNlXkEyXkFqcGdeQXVyMTUxMTM3OTc1._V1_SX300.jpg",
        "IMDB Rating": 6.6,
        "imdbID": "tt14993250",
        "Reasoning": "This movie is a romantic love story, which matches your query 'Romance/Love'."
    },
    {
        "Title": "3 Idiots",
        "Plot": "Farhan Qureshi and Raju Rastogi want to re-unite...",
        "Runtime": "170 min",
        "Release Year": 2009,
        "Actor": "Aamir Khan, Madhavan, Mona Singh",
        "Director": "Rajkumar Hirani",
        "Website": "https://www.primevideo.com/detail/3-Idiots/0LH1GMRIWABG6AFSW62O3BJJHH",
        "Poster": "https://m.media-amazon.com/images/M/MV5BNTkyOGVjMGEtNmQzZi00NzFlLTlhOWQtODYyMDc2ZGJmYzFhXkEyXkFqcGdeQXVyNjU0OTQ0OTY@._V1_SX300.jpg",
        "IMDB Rating": 8.4,
        "imdbID": "tt1187043",
        "Reasoning": "Although this movie is not primarily a romance, it has romantic elements and themes that match your query 'Romance/Love'."
    }
]

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

@bot.command(name='rag-movie-recomm')
async def movie_recomm(ctx):
    for movie in recommendations:
        embed = discord.Embed(title=movie["Title"], description=f"IMDB Rating: {movie['IMDB Rating']}\nReason: {movie['Reasoning']}")
        embed.set_image(url=movie["Poster"])
        view = View()
        if movie["Website"] != "N/A":
            button = Button(label="Watch Now", url=movie["Website"])
            view.add_item(button)
        await ctx.send(embed=embed, view=view)

@bot.command(name='movie-details')
async def movie_details(ctx, *, movie_title):
    movie = next((m for m in recommendations if m["Title"].lower() == movie_title.lower()), None)
    
    if not movie:
        await ctx.send("Movie not found!")
        return
    
    embed = discord.Embed(
    title=movie["Title"],
    description=movie["Plot"],
    color=discord.Color.yellow()
    )

    embed.add_field(name="Runtime", value=movie["Runtime"], inline=True)
    embed.add_field(name="Release Year", value=movie["Release Year"], inline=True)
    embed.add_field(name="IMDB Rating", value=str(movie["IMDB Rating"]), inline=True)
    embed.add_field(name="Actors", value=movie["Actor"], inline=True)
    embed.add_field(name="Director", value=movie["Director"], inline=True)
    embed.add_field(name="imdbID", value=str(movie["imdbID"]), inline=True)

    embed.add_field(name="Reasoning", value=movie["Reasoning"], inline=False)
    
    embed.set_image(url=movie["Poster"])

    view = View()
    if movie["Website"] != "-":
        button = Button(label="Watch Now", url=movie["Website"], style=discord.ButtonStyle.link)
        view.add_item(button)
    
    await ctx.send(embed=embed, view=view)

bot.run(TOKEN)

