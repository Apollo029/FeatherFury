# commands/reinforce.py
from discord import app_commands

def reinforce(interaction: discord.Interaction):
    # This function will be called as a method in core/bot.py
    pass  # Logic will be moved to core/bot.py

@app_commands.command(name="reinforce", description="Boost your strength in an active battle")
async def reinforce(interaction: discord.Interaction):
    await interaction.response.defer()
    user = interaction.user
    battle_id = None
    for bid, battle in bot.active_battles.items():
        if user in [battle["player1"].user, battle["player2"].user]:
            battle_id = bid
            break
    if not battle_id:
        await interaction.followup.send(f"{user.mention}, you are not in an active battle!")
        return
    battle = bot.active_battles[battle_id]
    player = battle["player1"] if user == battle["player1"].user else battle["player2"]
    # Apply a temporary buff (e.g., +10% attack for 3 turns)
    if "reinforce_buff" not in battle:
        battle["reinforce_buff"] = {}
    battle["reinforce_buff"][user.id] = {
        "attack_boost": 1.1,  # 10% attack increase
        "turns_remaining": 3
    }
    await battle["thread"].send(f"{user.mention} reinforces their troops! +10% attack for 3 turns.")
    await interaction.followup.send(f"{user.mention}, you have reinforced your troops!")
