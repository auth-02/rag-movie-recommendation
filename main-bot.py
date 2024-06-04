import os
import discord
from discord.ext import commands
from discord.ui import Button, View
from dotenv import load_dotenv
from recommend_movies import *
import json

embeddings = OllamaEmbeddings(model="llama3")
index_name="rag-movie-recomm"

pinecone_api_key = os.getenv("PINECONE_API_KEY")
pc = Pinecone(api_key=pinecone_api_key)


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)



@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    
@bot.command(name='recommend')
async def recommend_movies(ctx, *, query):
    
    qa = GeneralQuestionAnswering()
    docsearch = PineconeVectorStore.from_existing_index(index_name, embeddings)
    docs = docsearch.similarity_search(query)
    
    response = qa.ask_question(query, docs)
    print(response)

    json_data = response[response.find("["):response.rfind("]") + 1]
    recommendations = json.loads(json_data)
    print(recommendations)

    for movie in recommendations:
        # embed = discord.Embed(title=movie["Title"], description=f"IMDB Rating: {movie['IMDB Rating']}\nReason: {movie['Reasoning']}")
        # embed.set_image(url=movie["Poster"])
        # view = View()
        # if movie["Website"] != "":
        #     button = Button(label="Watch Now", url=movie["Website"])
        #     view.add_item(button)
        
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
        default_url = "https://www.imdb.com/title/tt1187043/"
        button = Button(label="Watch Now", url=movie["Website"] if movie["Website"] != "N/A" else default_url, style=discord.ButtonStyle.link)
        view.add_item(button)
        # button = Button(label="Watch Now", url=movie["Website"], style=discord.ButtonStyle.link)
        # view.add_item(button)
            
            
        await ctx.send(embed=embed, view=view)

bot.run(TOKEN)