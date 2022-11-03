import os
import discord
from dotenv import load_dotenv
import aiohttp
import nest_asyncio

load_dotenv()
nest_asyncio.apply()

TOKEN = os.getenv("DISCORD_TOKEN")
OPENAI_KEY = os.getenv("OPENAI_API_KEY")
client = discord.Client()

async def get_response(prompt):
    compliment = {
        'prompt': prompt,
        'temperature': 0.9,
        'max_tokens': 150,
        'top_p': 1,
        'frequency_penalty': 0,
        'presence_penalty': 0
    }
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False), headers={'authorization': f"Bearer {OPENAI_KEY}"}) as session:
        url = 'https://api.openai.com/v1/engines/text-davinci-002/completions'
        async with session.post(url, json=compliment) as resp:
            text = await resp.json()
            return text['choices'][0]['text']
    

@client.event
async def on_message(message):
    name = ""
    reason = ""
    if message.content == "%help compliment":
        await message.channel.send(f"```The correct format for a compliment is: \n'%compliment <name> for <reason>'```")
    if message.content.startswith("%compliment"):
        try:
            if "for" not in message.content:
                raise Exception
            text = str(message.content).split()[1:] 
            for i in range(len(text)):
                if text[i] == "for":
                    for j in range(len(text)-i):
                        try:
                            reason += text[j+i+1] + " "
                        except:
                            break
                    break
                name += text[i]
            p = f"Create a compliment using the following name and keywords\nName: {name}\nKeywords: {reason}"
            
            compliment = await get_response(p)
            
            await message.channel.send(compliment)
        except Exception as e:
            await message.channel.send(f"```Error Occurred.\nPlease refer to '%help compliment' to properly format your compliment``` {e}")
client.run(TOKEN)