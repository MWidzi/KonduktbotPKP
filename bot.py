import os
from database import Database
import discord
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")


class KonduktbotPkp(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True

        super().__init__(command_prefix="/", intents=intents)

        self.db = Database()

    async def setup_hook(self):
        await self.db.connect()

        for filename in os.listdir("./cogs"):
            if filename.endswith(".py"):
                await self.load_extension(f"cogs.{filename[:-3]}")
                print(f"Loaded extension: {filename}")

    async def close(self):
        await self.db.close()
        await super().close()


client = KonduktbotPkp()


@client.event
async def on_ready():
    print(f"We have logged in as user {client.user}")


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # Test path
    if message.content == "ping":
        await message.channel.send("pong")

    if message.content.startswith("## Rating"):
        authorRoles = message.author.roles
        eventRoles = await client.db.getEventRoles("rating")
        authorRoleIds = {str(role.id) for role in authorRoles}

        if not set(eventRoles).intersection(authorRoleIds):
            await message.reply("Próbujesz oceniać bez odpowiedniej roli!!!")
            return

        lines = message.content.splitlines()

        if lines:
            lines.pop(0)

        ratings = {}
        lineCounter = 1

        for line in lines:
            lineCounter += 1

            line.split()

            if not len(line) > 1:
                await message.reply(
                    f"Para klucz-wartość nie jest podana w linii {lineCounter}"
                )
                return

            ratings[filter(str.isalpha, line[0])] = line[1]

        await message.add_reaction("✅")


if TOKEN:
    client.run(TOKEN)
else:
    print("Error: DISCORD_TOKEN not found in environment or .env file.")
