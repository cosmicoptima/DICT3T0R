from core import client, debug_print
from language import add_cohere_token, tokens
from quests import Power, generate_quest, generate_boon

from discord import Interaction, Object, TextChannel, app_commands
import random
from traceback import format_exc

SPECIFIC_CHANNEL = 1039267300412493856

CELESTECORD = 1039267299863035964

tree = app_commands.CommandTree(client)


@client.event
async def on_ready():
    await tree.sync(guild=Object(id=CELESTECORD))

    channel = client.get_channel(SPECIFIC_CHANNEL)
    if isinstance(channel, TextChannel):
        await channel.send("hi")


@tree.command(
    name="restart",
    description="Restart to pull new changes.",
    guild=Object(id=CELESTECORD),
)
async def restart(interaction: Interaction):
    await interaction.response.send_message("I WILL RETURN!")
    exit(0)


@tree.command(
    name="sacrifice",
    description="Sacrifice a Cohere token to the gods.",
    guild=Object(id=CELESTECORD),
)
async def sacrifice(interaction: Interaction, token: str):
    if add_cohere_token(token):
        response = "Your sacrifice has been accepted."
    else:
        response = "That token is invalid."
    await interaction.response.send_message(response, ephemeral=True)


@tree.command(
    name="quest", description="Test command: make quest", guild=Object(id=CELESTECORD)
)
async def gen_quest_test(interaction: Interaction):
    await interaction.response.defer()

    try:
        quest = generate_quest()
        await interaction.followup.send(f"({quest.xp} exp) {quest.description}")
    except:
        debug_print(format_exc())


@tree.command(
    name="boon", description="Test command: make boon", guild=Object(id=CELESTECORD)
)
async def gen_boon_test(interaction: Interaction):
    await interaction.response.defer()
    try:
        boon = generate_boon(random.choice(list(Power)))
        await interaction.followup.send(f"({boon.strength}) {boon.description}")
    except:
        debug_print(format_exc())


client.run(tokens["discord"])
