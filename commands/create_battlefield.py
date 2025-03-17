# commands/create_battlefield.py
# commands/create_battlefield.py
from discord import app_commands
from data.battlefields import BATTLEFIELD_MODIFIERS, BATTLEFIELD_DESCRIPTIONS

def create_battlefield(interaction: discord.Interaction, name: str, effect: str, modifier: str):
    # This function will be called as a method in core/bot.py
    pass  # Logic will be moved to core/bot.py

@app_commands.command(name="create_battlefield", description="Create a new battlefield (admin only)")
@app_commands.checks.has_permissions(administrator=True)
@app_commands.describe(name="Name of the battlefield", effect="Description of the battlefield effect", modifier="Modifiers (e.g., Winged Creature:1.2,Aquatic Creature:0.9)")
async def create_battlefield(interaction: discord.Interaction, bot: discord.Client, name: str, effect: str, modifier: str):
    await interaction.response.defer()
    if name in BATTLEFIELD_MODIFIERS:
        await interaction.followup.send(f"Battlefield {name} already exists!")
        return
    modifier_dict = {}
    for mod in modifier.split(","):
        key, value = mod.split(":")
        modifier_dict[key.strip()] = float(value)
    BATTLEFIELD_MODIFIERS[name] = modifier_dict
    BATTLEFIELD_DESCRIPTIONS[name] = effect
    await interaction.followup.send(f"Created new battlefield {name} with effect '{effect}' and modifiers {modifier_dict}")

