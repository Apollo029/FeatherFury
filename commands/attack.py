# commands/attack.py
# commands/attack.py
from discord import app_commands
from datetime import datetime
import pytz
import unicodedata
from data.battlefields import BATTLEFIELD_MODIFIERS, BATTLEFIELD_DESCRIPTIONS
from data.attributes import attribute_emojis, ATTRIBUTE_ATTACKS
from data.classes import CLASS_ATTACKS
from data.class_types import Player, GENERIC_ATTACK
from data.constants import CHANNEL_CONFIGS
from utils.roles import assign_dead_role
from battle.state import initialize_battle_state

def attack(interaction: discord.Interaction, opponent: discord.Member):
    # This function will be called as a method in core/bot.py
    pass  # Logic will be moved to core/bot.py

@app_commands.command(name="attack", description="Start a battle with another user or bot")
@app_commands.describe(opponent="The user or bot to battle")
async def attack(interaction: discord.Interaction, bot: discord.Client, opponent: discord.Member):
    await interaction.response.defer()
    guild = interaction.guild
    user = interaction.user
    if user.id not in bot.global_player_profiles or not bot.global_player_profiles[user.id].get("class"):
        await interaction.followup.send(f"{user.mention}, you must select a class first in {CHANNEL_CONFIGS['class_channel']}!")
        return
    if opponent.id not in bot.global_player_profiles or not bot.global_player_profiles[opponent.id].get("class"):
        await interaction.followup.send(f"{opponent.mention} has not selected a class yet!")
        return
    dead_role = discord.utils.get(guild.roles, name="Dead")
    if dead_role in user.roles:
        await interaction.followup.send(f"{user.mention}, you are dead! You cannot start a battle until revived.")
        return
    if dead_role in opponent.roles:
        await interaction.followup.send(f"{opponent.mention} is dead and cannot be challenged!")
        return
    battle_channel_name = CHANNEL_CONFIGS["battlefield_channel"]
    normalized_target = ''.join(c for c in unicodedata.normalize('NFC', battle_channel_name) if not unicodedata.combining(c))
    battle_channel = discord.utils.get(guild.channels, name=normalized_target)
    if not battle_channel:
        try:
            battle_channel = await guild.create_text_channel(battle_channel_name)
            print(f"Created battle channel {battle_channel_name} in {guild.name}")
        except discord.Forbidden:
            await interaction.followup.send("I don't have permission to create a battle channel!")
            return
    bot.battle_counter += 1
    battle_id = f"battle_{bot.battle_counter}_{int(datetime.now(pytz.UTC).timestamp())}"
    player1 = Player(user, bot.global_player_profiles[user.id]["class"], bot.global_player_profiles[user.id]["attributes"], bot.global_player_profiles[user.id]["level"], bot.global_player_profiles[user.id]["race"], bot.global_player_profiles[user.id]["race_effects"])
    player2 = Player(opponent, bot.global_player_profiles[opponent.id]["class"], bot.global_player_profiles[opponent.id]["attributes"], bot.global_player_profiles[opponent.id]["level"], bot.global_player_profiles[opponent.id]["race"], bot.global_player_profiles[opponent.id]["race_effects"])
    bot.active_battles[battle_id] = initialize_battle_state(player1, player2, battle_channel, random.choice(list(BATTLEFIELD_MODIFIERS.keys())))
    await bot.active_battles[battle_id]["thread"].send(f"Battle started between {user.mention} and {opponent.mention} in {bot.active_battles[battle_id]['battlefield']}!\n{BATTLEFIELD_DESCRIPTIONS[bot.active_battles[battle_id]['battlefield']]}")
    turn_message = await bot.active_battles[battle_id]["thread"].send(f"{user.mention}'s turn! React with an attribute, ⚔️, or 🛡️ to act.")
    for attr in player1.attributes:
        if attr in ATTRIBUTE_ATTACKS:
            emoji = attribute_emojis.get(attr, "❓")
            await turn_message.add_reaction(emoji)
    await turn_message.add_reaction("⚔️")
    await turn_message.add_reaction("🛡️")
    bot.active_battles[battle_id]["message"] = turn_message
    bot.reaction_processed[battle_id] = set()
