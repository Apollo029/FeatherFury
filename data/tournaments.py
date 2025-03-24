# data/tournaments.py
import random
from datetime import datetime
import pytz
from data.constants import XP_PER_TOURNAMENT_WIN, XP_PER_TOURNAMENT_LOSS

def start_monthly_tournament(bot, guild):
    participants = [member for member in guild.members if member.id in bot.global_player_profiles and bot.global_player_profiles[member.id].get("class")]
    if len(participants) < 2:
        return "Not enough participants for a monthly tournament!"
    random.shuffle(participants)
    bracket = [(participants[i], participants[i+1]) for i in range(0, len(participants)-1, 2)]
    bot.tournament_active = True
    bot.tournament_bracket[guild.id] = bracket
    return f"Monthly tournament started in {guild.name}! {len(participants)} participants, {len(bracket)} matches in the first round."

def start_quarterly_tournament(bot, guild):
    participants = [member for member in guild.members if member.id in bot.global_player_profiles and bot.global_player_profiles[member.id].get("class")]
    if len(participants) < 2:
        return "Not enough participants for a quarterly tournament!"
    battle_type = random.choice(["1v1", "team", "king_of_the_hill"])
    bot.tournament_active = True
    bot.tournament_bracket[guild.id] = {"type": battle_type, "participants": participants, "round": 1}
    return f"Quarterly tournament started in {guild.name}! Type: {battle_type}, {len(participants)} participants."

def process_tournament_round(bot, guild):
    bracket = bot.tournament_bracket.get(guild.id, [])
    if not bracket:
        return "No active tournament in this guild!"
    if isinstance(bracket, dict):  # Quarterly tournament
        battle_type = bracket["type"]
        participants = bracket["participants"]
        round_num = bracket["round"]
        if battle_type == "1v1":
            if len(participants) <= 1:
                winner = participants[0] if participants else None
                bot.tournament_active = False
                bot.tournament_bracket[guild.id] = {}
                bot.tournament_winner = winner
                if winner:
                    winner_profile = bot.global_player_profiles[winner.id]
                    winner_profile["stats"]["quarterly_trophies"] += 1
                    winner_profile["xp"] += XP_PER_TOURNAMENT_WIN
                    winner_profile["battle_tokens"][str(guild.id)] = min(winner_profile["battle_tokens"][str(guild.id)] + 10, 20)  # +10 tokens
                    from core.events import update_stats_embed
                    await update_stats_embed(bot, guild, winner.id)
                return f"Tournament ended! Winner: {winner.mention if winner else 'None'}"
            matches = [(participants[i], participants[i+1]) for i in range(0, len(participants)-1, 2)]
            bot.tournament_bracket[guild.id]["matches"] = matches
            return f"Round {round_num} started with {len(matches)} matches!"
        elif battle_type == "team":
            # Placeholder for team battles
            return "Team battles will be implemented in a future phase."
        else:  # king_of_the_hill
            if len(participants) <= 1:
                winner = participants[0] if participants else None
                bot.tournament_active = False
                bot.tournament_bracket[guild.id] = {}
                bot.tournament_winner = winner
                if winner:
                    winner_profile = bot.global_player_profiles[winner.id]
                    winner_profile["stats"]["quarterly_trophies"] += 1
                    winner_profile["xp"] += XP_PER_TOURNAMENT_WIN
                    winner_profile["battle_tokens"][str(guild.id)] = min(winner_profile["battle_tokens"][str(guild.id)] + 10, 20)  # +10 tokens
                    from core.events import update_stats_embed
                    await update_stats_embed(bot, guild, winner.id)
                return f"Tournament ended! Winner: {winner.mention if winner else 'None'}"
            match_participants = random.sample(participants, min(5, len(participants)))
            bot.tournament_bracket[guild.id]["matches"] = [match_participants]
            return f"Round {round_num} started with a King of the Hill match: {', '.join(p.mention for p in match_participants)}!"
    else:  # Monthly tournament
        if not bracket:
            bot.tournament_active = False
            bot.tournament_bracket[guild.id] = {}
            return "Tournament ended! No winner (all matches completed)."
        # Placeholder for match simulation
        winner = random.choice([match[0], match[1]])
        loser = match[0] if winner == match[1] else match[1]
        winner_profile = bot.global_player_profiles[winner.id]
        loser_profile = bot.global_player_profiles[loser.id]
        winner_profile["stats"]["wins"] += 1
        winner_profile["xp"] += XP_PER_TOURNAMENT_WIN
        winner_profile["battle_tokens"][str(guild.id)] = min(winner_profile["battle_tokens"][str(guild.id)] + 5, 20)  # +5 tokens
        loser_profile["stats"]["losses"] += 1
        loser_profile["xp"] += XP_PER_TOURNAMENT_LOSS
        from core.events import update_stats_embed
        await update_stats_embed(bot, guild, winner.id)
        await update_stats_embed(bot, guild, loser.id)
        new_bracket = bracket[1:]
        bot.tournament_bracket[guild.id] = new_bracket
        return f"Match ended! {winner.mention} defeated {loser.mention}!"
