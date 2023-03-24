from discord import Client, Intents, Object, Interaction, app_commands
from openai import ChatCompletion
import cohere
import logging
import language
import quests
import openai
import json

CELESTECORD = 1039267299863035964

intents = Intents.default()
intents.members = True
intents.message_content = True
client = Client(intents=intents)
tree = app_commands.CommandTree(client)
        

@client.event
async def on_ready():
    await tree.sync(guild = Object(id=CELESTECORD))

@tree.command(
    name = "restart",
    description = "Restart to pull new changes.",
    guild = Object(id=CELESTECORD)
)
async def restart(interaction: Interaction):
    await interaction.response.send_message("I WILL RETURN!")
    exit(0)

@tree.command(
    name = "quest",
    description = "Test command: make quest",
    guild = Object(id=CELESTECORD)
)
async def genqcmd(interaction: Interaction):
    await interaction.response.defer()
    try:
        quest = quests.generate_quest()
        await interaction.followup.send(f"({quest.exp} exp) {quest.desc}")
    except Exception as e:
        await interaction.followup.send(str(e))
        raise e


@tree.command(
    name = "boon",
    description = "Test command: make boon",
    guild = Object(id=CELESTECORD)
)
async def genbcmd(interaction: Interaction):
    await interaction.response.defer()
    try:
        boon = quests.generate_boon(quests.Strength.MEDIUM)
        await interaction.followup.send(boon)
    except Exception as e:
        await interaction.followup.send(str(e))
        raise e


client.run(language.tokens["discord"])