# commands/create_class.py
from discord import app_commands
from data.classes import CLASS_STATS, CLASS_ATTACKS

def create_class(interaction: discord.Interaction, name: str, emoji: str, hp: int, attack: int, defense: int, description: str):
    # This function will be called as a method in core/bot.py
    pass  # Logic will be moved to core/bot.py

@app_commands.command(name="create_class", description="Create a new class (admin only)")
@app_commands.checks.has_permissions(administrator=True)
@app_commands.describe(name="Name of the class", emoji="Emoji for the class", hp="Base HP", attack="Base attack", defense="Base defense", description="Class description")
async def create_class(interaction: discord.Interaction, bot: discord.Client, name: str, emoji: str, hp: int, attack: int, defense: int, description: str):
    await interaction.response.defer()
    if name in CLASS_STATS:
        await interaction.followup.send(f"Class {name} already exists!")
        return
    CLASS_STATS[name] = {
        "emoji": emoji,
        "hp": hp,
        "attack": attack,
        "defense": defense,
        "speed": 15,  # Default speed
        "description": description
    }
    CLASS_ATTACKS[name] = {"name": f"{name} Strike", "damage_range": (15, 25), "effect": f"Standard {name} attack"}
    await interaction.followup.send(f"Created new class {name} with stats: HP {hp}, Attack {attack}, Defense {defense}, Description: {description}")

