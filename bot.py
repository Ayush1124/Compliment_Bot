import os
import discord
import openai
from dotenv import load_dotenv
import sys

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
openai.api_key = os.getenv("OPENAI_API_KEY")
client = discord.Client()

@client.event
async def on_message(message):
    name = ""
    reason = ""
    if message.content == "%help compliment":
        await message.channel.send(f"```The correct format for a compliment is: \n'%compliment <name> for <reason>'```")
    if message.content.startswith("%compliment"):
        try:
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
            response = openai.Completion.create(
                model="text-davinci-002",
                prompt= p,
                temperature=0.7,
                max_tokens=256,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
            )
            await message.channel.send(response["choices"][0]["text"])
        except:
            await message.channel.send(f"```Error Occurred.\nPlease refer to '%help compliments' to properly format your compliment\n{sys.exc_info()}```")
client.run(TOKEN)