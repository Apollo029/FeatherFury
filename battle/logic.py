# battle/logic.py
import random
from data.class_types import Player, GENERIC_ATTACK

async def apply_status_effects(battle, player):
    if player.user.id not in battle["status_effects"]:
        return
    effects = battle["status_effects"][player.user.id]
    if "poison" in effects:
        effects["poison"] -= 1
        if effects["poison"] <= 0:
            del effects["poison"]
        else:
            player.hp -= 5
            await battle["thread"].send(f"{player.user.mention} takes 5 poison damage! HP: {player.hp}")
    if "burn" in effects:
        effects["burn"] -= 1
        if effects["burn"] <= 0:
            del effects["burn"]
        else:
            player.hp -= 5
            await battle["thread"].send(f"{player.user.mention} takes 5 burn damage! HP: {player.hp}")
    if "vulnerable" in effects:
        del effects["vulnerable"]
    if "stun" in effects:
        del effects["stun"]
    if player.hp <= 0:
        player.alive = False
        player.hp = 0

async def apply_poison_effect(battle, player):
    if player.user.id in battle["status_effects"] and "poison" in battle["status_effects"][player.user.id]:
        await apply_status_effects(battle, player)

async def apply_burn_effect(battle, player):
    if player.user.id in battle["status_effects"] and "burn" in battle["status_effects"][player.user.id]:
        await apply_status_effects(battle, player)

async def apply_vulnerable_effect(battle, player):
    if player.user.id in battle["status_effects"] and "vulnerable" in battle["status_effects"][player.user.id]:
        battle["status_effects"][player.user.id]["vulnerable"] = 0

async def apply_stun_effect(battle, player, battle_id, bot):
    if player.user.id in battle["status_effects"] and "stun" in battle["status_effects"][player.user.id]:
        await battle["thread"].send(f"{player.user.mention} is stunned and skips their turn!")
        del battle["status_effects"][player.user.id]["stun"]
        battle["round_active"] = False
        await asyncio.sleep(5)
        battle["round_active"] = True
        opponent = battle["player1"] if player == battle["player2"] else battle["player2"]
        turn_message = await battle["thread"].send(f"{opponent.user.mention}'s turn! React with an attribute, ⚔️, or 🛡️ to act.")
        for attr in opponent.attributes:
            if attr in ATTRIBUTE_ATTACKS:
                emoji = attribute_to_emoji.get(attr, "❓")
                await turn_message.add_reaction(emoji)
        await turn_message.add_reaction("⚔️")
        await turn_message.add_reaction("🛡️")
        battle["message"] = turn_message
        bot.reaction_processed[battle_id] = set()
        return True
    return False

