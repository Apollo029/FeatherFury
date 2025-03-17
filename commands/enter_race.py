# commands/enter_race.py
from discord import app_commands
from data.class_types import generate_race_effects

def enter_race(interaction: discord.Interaction, name: str, color: str):
    # This function will be called as a method in core/bot.py
    pass  # Logic will be moved to core/bot.py

@app_commands.command(name="enter_race", description="Enter a race with a custom name and color")
@app_commands.describe(name="The name of your race", color="The color of your race (e.g., red, green, blue)")
async def enter_race(interaction: discord.Interaction, bot: discord.Client, name: str, color: str):
    await interaction.response.defer()
    guild = interaction.guild
    user = interaction.user
    if user.id in bot.global_player_profiles and bot.global_player_profiles[user.id].get("race"):
        await interaction.followup.send(f"{user.mention}, you have already entered a race! Ask an admin to reset it if needed.")
        return
    race_effects = generate_race_effects(name, color)
    bot.global_player_profiles[user.id] = bot.global_player_profiles.get(user.id, {
        "class": None,
        "attributes": [],
        "race": name,
        "stats": {
            "wins": 0,
            "losses": 0,
            "total_battles": 0,
            "total_damage_dealt": 0,
            "total_damage_taken": 0,
            "critical_hits": 0,
            "critical_wins": 0,
            "bots_beaten": 0,
            "losses_to_bots": 0
        },
        "level": 1,
        "xp": 0,
        "race_effects": race_effects
    })
    bot.global_player_profiles[user.id]["race"] = name
    bot.global_player_profiles[user.id]["race_effects"] = race_effects
    try:
        role = await guild.create_role(name=name, color=discord.Color.from_str(color if color.startswith("#") else {"red": 0xFF0000, "green": 0x00FF00, "blue": 0x0000FF}.get(color.lower(), 0xFFFFFF)))
        await user.add_roles(role)
        await interaction.followup.send(f"Successfully completed /EnterRace for {user.name} with race {name} and effects {race_effects['effects']}")
    except discord.HTTPException as e:
        await interaction.followup.send(f"Failed to create role for race {name}: {e}")

