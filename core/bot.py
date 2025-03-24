# core/bot.py
import discord
import random
from discord import app_commands
import schedule
import asyncio
from datetime import datetime
import pytz
import unicodedata
from discord.ui import Select, View
from core.events import on_ready, on_message, on_reaction_add, update_stats_embed
from data.battlefields import BATTLEFIELD_MODIFIERS, BATTLEFIELD_DESCRIPTIONS
from data.attributes import attribute_emojis, ATTRIBUTE_ATTACKS, PRIMARY_ATTRIBUTES, attribute_emoji_fallbacks
from data.classes import CLASS_ATTACKS, CLASS_STATS
from data.class_types import Player, generate_race_effects
from data.constants import CHANNEL_CONFIGS
from utils.roles import assign_dead_role
from battle.state import initialize_battle_state

class FeatherFuryBot(discord.Client):
    def __init__(self):
        print("Initializing FeatherFuryBot...")
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        intents.reactions = True
        intents.messages = True
        intents.message_content = True
        print("Intents configured:", intents)
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)
        self.bot_name = "FeatherFury"
        self.global_player_profiles = {}
        self.active_battles = {}
        self.battle_counter = 0
        self.class_selection_message = {}
        self.attribute_selection_message = {}
        self.race_selection_message = {}
        self.stats_message_ids = {}
        self.tournament_active = False
        self.tournament_bracket = {}
        self.tournament_winner = None
        self.custom_attack_duration = 2
        self.current_quarter = (datetime.now(pytz.UTC).month - 1) // 3 + 1
        self.reaction_processed = {}
        print("Bot attributes initialized")

    async def setup_hook(self):
        print("Syncing command tree...")
        self.tree.add_command(app_commands.Command(name="attack", description="Start a battle with another user or bot", callback=self.attack))
        self.tree.add_command(app_commands.Command(name="reinforce", description="Boost your strength in an active battle", callback=self.reinforce))
        self.tree.add_command(app_commands.Command(name="edit_bot_profile", description="Edit a bot's profile (admin only)", callback=self.edit_bot_profile))
        self.tree.add_command(app_commands.Command(name="reset_class", description="Reset a user's class and race (admin only)", callback=self.reset_class))
        self.tree.add_command(app_commands.Command(name="enter_race", description="Enter a race with a custom name and color", callback=self.enter_race))
        self.tree.add_command(app_commands.Command(name="remove_race", description="Remove a user's race (admin only)", callback=self.remove_race))
        self.tree.add_command(app_commands.Command(name="remove_attribute", description="Remove an attribute from a user (admin only)", callback=self.remove_attribute))
        self.tree.add_command(app_commands.Command(name="create_attribute", description="Create a new attribute (admin only)", callback=self.create_attribute))
        self.tree.add_command(app_commands.Command(name="create_battlefield", description="Create a new battlefield (admin only)", callback=self.create_battlefield))
        self.tree.add_command(app_commands.Command(name="create_class", description="Create a new class (admin only)", callback=self.create_class))
        self.tree.add_command(app_commands.Command(name="stats", description="View your stats or another user's stats", callback=self.stats))
        try:
            print("Starting global command sync...")
            await self.tree.sync()
            print("Command tree synced successfully (global).")
            for guild in self.guilds:
                print(f"Syncing commands for guild: {guild.name} (ID: {guild.id})")
                try:
                    await self.tree.sync(guild=guild)
                    print(f"Successfully synced commands for guild {guild.name}")
                except Exception as e:
                    print(f"Failed to sync commands for guild {guild.name}: {e}")
            await asyncio.sleep(5)
        except Exception as e:
            print(f"Failed to sync command tree (global): {e}")
        print("Available global commands:", [command.name for command in self.tree.get_commands()])

    async def check_admin(interaction: discord.Interaction):
        admin_role = discord.utils.get(interaction.guild.roles, name="Admin")
        if not admin_role:
            raise app_commands.errors.CheckFailure("No 'Admin' role found in the server!")
        if admin_role in interaction.user.roles:
            return True
        raise app_commands.errors.CheckFailure("You need the 'Admin' role to run this command!")

    @app_commands.describe(opponent="The user or bot to battle")
    async def attack(self, interaction: discord.Interaction, opponent: discord.Member):
        await interaction.response.defer()
        guild = interaction.guild
        user = interaction.user
        if user.id not in self.global_player_profiles or not self.global_player_profiles[user.id].get("class"):
            await interaction.followup.send(f"{user.mention}, you must select a class first in {CHANNEL_CONFIGS['class_channel']}!")
            return
        if opponent.id not in self.global_player_profiles or not self.global_player_profiles[opponent.id].get("class"):
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
        battle_channel = discord.utils.get(guild.text_channels, name=battle_channel_name.lstrip('#'))
        if not battle_channel:
            try:
                battle_channel = await guild.create_text_channel(battle_channel_name)
                print(f"Created battlefield channel {battle_channel_name} in {guild.name}")
            except discord.Forbidden:
                await interaction.followup.send("I don't have permission to create a battlefield channel!")
                return
        print(f"Using battlefield channel: {battle_channel.name} (ID: {battle_channel.id})")
        thread_name = f"Battle-{user.display_name}-vs-{opponent.display_name}-{self.battle_counter}"
        try:
            thread = await battle_channel.create_thread(name=thread_name, auto_archive_duration=60)
            print(f"Created thread {thread.name} in {battle_channel.name} (ID: {thread.id})")
        except discord.Forbidden:
            await interaction.followup.send("I don't have permission to create threads!")
            return
        self.battle_counter += 1
        battle_id = f"battle_{self.battle_counter}_{int(datetime.now(pytz.UTC).timestamp())}"
        player1 = Player(user, self.global_player_profiles[user.id]["class"], self.global_player_profiles[user.id]["attributes"], self.global_player_profiles[user.id]["level"], self.global_player_profiles[user.id]["race"], self.global_player_profiles[user.id]["race_effects"])
        player2 = Player(opponent, self.global_player_profiles[opponent.id]["class"], self.global_player_profiles[opponent.id]["attributes"], self.global_player_profiles[opponent.id]["level"], self.global_player_profiles[opponent.id]["race"], self.global_player_profiles[opponent.id]["race_effects"])
        print(f"Player1 stats: hp={player1.hp}/{player1.max_hp}, attack={player1.attack}, defense={player1.defense}, speed={player1.speed}")
        print(f"Player2 stats: hp={player2.hp}/{player2.max_hp}, attack={player2.attack}, defense={player2.defense}, speed={player2.speed}")
        self.active_battles[battle_id] = initialize_battle_state(player1, player2, thread, random.choice(list(BATTLEFIELD_MODIFIERS.keys())))
        await self.active_battles[battle_id]["thread"].send(f"Battle started between {user.mention} and {opponent.mention} in {self.active_battles[battle_id]['battlefield']}!\n{BATTLEFIELD_DESCRIPTIONS[self.active_battles[battle_id]['battlefield']]}")
        turn_message = await self.active_battles[battle_id]["thread"].send(f"{user.mention}'s turn! React with an attribute, ⚔️, or 🛡️ to act.")
        for attr in player1.attributes:
            if attr in ATTRIBUTE_ATTACKS:
                emoji = attribute_emojis.get(attr, "❓")
                await turn_message.add_reaction(emoji)
        await turn_message.add_reaction("⚔️")
        await turn_message.add_reaction("🛡️")
        self.active_battles[battle_id]["message"] = turn_message
        self.reaction_processed[battle_id] = set()

    async def reinforce(self, interaction: discord.Interaction):
        await interaction.response.defer()
        user = interaction.user
        battle_id = None
        for bid, battle in self.active_battles.items():
            if user in [battle["player1"].user, battle["player2"].user]:
                battle_id = bid
                break
        if not battle_id:
            await interaction.followup.send(f"{user.mention}, you are not in an active battle!")
            return
        battle = self.active_battles[battle_id]
        player = battle["player1"] if user == battle["player1"].user else battle["player2"]
        if "reinforce_buff" not in battle:
            battle["reinforce_buff"] = {}
        battle["reinforce_buff"][user.id] = {"attack_boost": 1.1, "turns_remaining": 3}
        await battle["thread"].send(f"{user.mention} reinforces their troops! +10% attack for 3 turns.")
        await interaction.followup.send(f"{user.mention}, you have reinforced your troops!")

    @app_commands.check(check_admin)
    @app_commands.describe(bot_user="The bot to edit", class_type="The bot's new class", attributes="Comma-separated attributes (e.g., Fire,Water,Ice)")
    async def edit_bot_profile(self, interaction: discord.Interaction, bot_user: discord.Member, class_type: str, attributes: str):
        await interaction.response.defer()
        if not bot_user.bot:
            await interaction.followup.send(f"{bot_user.mention} is not a bot!")
            return
        if class_type not in CLASS_STATS and class_type != "All Classes":
            await interaction.followup.send(f"Invalid class type {class_type}. Available: {', '.join(CLASS_STATS.keys())}")
            return
        attr_list = [attr.strip() for attr in attributes.split(",")]
        if len(attr_list) > 3:
            await interaction.followup.send("A bot can only have up to 3 attributes!")
            return
        for attr in attr_list:
            if attr not in PRIMARY_ATTRIBUTES:
                await interaction.followup.send(f"Invalid attribute {attr}. Available: {', '.join(PRIMARY_ATTRIBUTES)}")
                return
        self.global_player_profiles[bot_user.id] = {
            "class": class_type,
            "attributes": attr_list,
            "race": self.global_player_profiles.get(bot_user.id, {}).get("race", "BotRace_1"),
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
            "level": self.global_player_profiles.get(bot_user.id, {}).get("level", 1),
            "xp": 0,
            "race_effects": self.global_player_profiles.get(bot_user.id, {}).get("race_effects", {"effects": [], "power_index": 0})
        }
        await interaction.followup.send(f"Updated profile for {bot_user.mention}: Class: {class_type}, Attributes: {attr_list}")
        await update_stats_embed(self, interaction.guild, bot_user.id)

    @app_commands.check(check_admin)
    @app_commands.describe(user="The user whose class and race to reset")
    async def reset_class(self, interaction: discord.Interaction, user: discord.Member):
        await interaction.response.defer()
        guild = interaction.guild
        if user.id not in self.global_player_profiles:
            await interaction.followup.send(f"{user.mention} has no profile to reset!")
            return
        current_class = self.global_player_profiles[user.id].get("class")
        current_race = self.global_player_profiles[user.id].get("race")
        self.global_player_profiles[user.id] = {
            "class": None,
            "attributes": [],
            "race": None,
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
            "race_effects": {"effects": [], "power_index": 0}
        }
        class_role = discord.utils.get(guild.roles, name=current_class) if current_class else None
        race_role = discord.utils.get(guild.roles, name=current_race) if current_race else None
        if class_role and class_role in user.roles:
            try:
                await user.remove_roles(class_role)
                print(f"Removed class role {current_class} from {user.display_name}")
            except discord.Forbidden:
                await interaction.followup.send(f"Failed to remove class role {current_class} due to permissions!")
                return
        if race_role and race_role in user.roles:
            try:
                await user.remove_roles(race_role)
                print(f"Removed race role {current_race} from {user.display_name}")
            except discord.Forbidden:
                await interaction.followup.send(f"Failed to remove race role {current_race} due to permissions!")
                return
        await interaction.followup.send(f"Reset class and race for {user.mention}!")
        await update_stats_embed(self, guild, user.id)

@app_commands.describe(name="The name of your race", color="The color of your race (e.g., red, #000000, 000000)")
async def enter_race(self, interaction: discord.Interaction, name: str, color: str):
    await interaction.response.defer()
    guild = interaction.guild
    user = interaction.user
    profile = self.global_player_profiles.get(user.id, {})
    class_type = profile.get("class")
    attributes = profile.get("attributes", [])
    if user.id in self.global_player_profiles and self.global_player_profiles[user.id].get("race"):
        await interaction.followup.send(f"{user.mention}, you have already entered a race! Ask an admin to reset it if needed.")
        return
    race_effects = generate_race_effects(name, color, class_type=class_type, attributes=attributes)
    self.global_player_profiles[user.id] = self.global_player_profiles.get(user.id, {
        "class": class_type,
        "attributes": attributes,
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
        "level": profile.get("level", 1),
        "xp": profile.get("xp", 0),
        "race_effects": race_effects,
        "race_color": color  # Store the race color
    })
    try:
        hex_color = color
        if not color.startswith("#"):
            color_map = {
                "red": "#FF0000",
                "green": "#00FF00",
                "blue": "#0000FF",
                "white": "#FFFFFF",
                "black": "#000000",
                "yellow": "#FFFF00",
                "purple": "#800080",
                "orange": "#FFA500",
                "pink": "#FFC0CB",
                "cyan": "#00FFFF"
            }
            hex_color = color_map.get(color.lower(), "#FFFFFF")
            if len(color) == 6 and all(c in '0123456789ABCDEFabcdef' for c in color):
                hex_color = f"#{color}"
        try:
            discord.Color.from_str(hex_color)
        except ValueError:
            await interaction.followup.send(f"Invalid color format for '{color}'. Use a color name (e.g., red, blue) or a hex code (e.g., #FF0000 or 000000).")
            return
        role = await guild.create_role(name=name, color=discord.Color.from_str(hex_color))
        await user.add_roles(role)
        self.global_player_profiles[user.id]["race_color"] = hex_color  # Ensure color is stored
        confirmation = await interaction.followup.send(f"Successfully completed /EnterRace for {user.display_name} with race {name} and effects {race_effects['effects']}")
        await asyncio.sleep(10)
        await confirmation.delete()
        await update_stats_embed(self, guild, user.id)
    except discord.HTTPException as e:
        await interaction.followup.send(f"Failed to create role for race {name}: {e}")

    @app_commands.check(check_admin)
    @app_commands.describe(user="The user whose race to remove")
    async def remove_race(self, interaction: discord.Interaction, user: discord.Member):
        await interaction.response.defer()
        if user.id not in self.global_player_profiles or not self.global_player_profiles[user.id].get("race"):
            await interaction.followup.send(f"{user.mention} has no race to remove!")
            return
        race = self.global_player_profiles[user.id]["race"]
        race_role = discord.utils.get(interaction.guild.roles, name=race)
        if race_role and race_role in user.roles:
            try:
                await user.remove_roles(race_role)
                print(f"Removed race role {race} from {user.display_name}")
            except discord.Forbidden:
                await interaction.followup.send(f"Failed to remove race role {race} due to permissions!")
                return
        self.global_player_profiles[user.id]["race"] = None
        self.global_player_profiles[user.id]["race_effects"] = {"effects": [], "power_index": 0}
        await interaction.followup.send(f"Removed race {race} from {user.mention}!")
        await update_stats_embed(self, guild, user.id)

    @app_commands.check(check_admin)
    @app_commands.describe(user="The user whose attribute to remove")
    async def remove_attribute(self, interaction: discord.Interaction, user: discord.Member):
        await interaction.response.defer()
        if user.id not in self.global_player_profiles or not self.global_player_profiles[user.id].get("attributes"):
            await interaction.followup.send(f"{user.mention} has no attributes to remove!")
            return
        attributes = self.global_player_profiles[user.id]["attributes"]
        if not attributes:
            await interaction.followup.send(f"{user.mention} has no attributes to remove!")
            return
        options = [discord.SelectOption(label=attr, value=attr) for attr in attributes]
        select = Select(placeholder="Select an attribute to remove", options=options)

        async def select_callback(interaction: discord.Interaction):
            selected_attribute = select.values[0]
            attributes.remove(selected_attribute)
            self.global_player_profiles[user.id]["attributes"] = attributes
            attribute_role = discord.utils.get(interaction.guild.roles, name=selected_attribute)
            if attribute_role and attribute_role in user.roles:
                try:
                    await user.remove_roles(attribute_role)
                    print(f"Removed attribute role {selected_attribute} from {user.display_name}")
                except discord.Forbidden:
                    await interaction.followup.send(f"Failed to remove attribute role {selected_attribute} due to permissions!")
                    return
            await interaction.response.send_message(f"Removed {selected_attribute} from {user.mention}!")
            await update_stats_embed(self, interaction.guild, user.id)

        select.callback = select_callback
        view = View()
        view.add_item(select)
        await interaction.followup.send(f"Select an attribute to remove from {user.mention}:", view=view)

    @app_commands.check(check_admin)
    @app_commands.describe(name="Name of the new attribute", emoji="Emoji for the new attribute")
    async def create_attribute(self, interaction: discord.Interaction, name: str, emoji: str):
        await interaction.response.defer()
        if name in PRIMARY_ATTRIBUTES:
            await interaction.followup.send(f"Attribute {name} already exists!")
            return
        PRIMARY_ATTRIBUTES.append(name)
        attribute_emojis[emoji] = name
        attribute_emoji_fallbacks[name] = emoji.strip(":") if emoji.startswith(":") and emoji.endswith(":") else name.lower()
        await interaction.followup.send(f"Created new attribute {name} with emoji {emoji}")

    @app_commands.check(check_admin)
    @app_commands.describe(name="Name of the battlefield", effect="Description of the battlefield effect", modifier="Modifiers (e.g., Winged Creature:1.2,Aquatic Creature:0.9)")
    async def create_battlefield(self, interaction: discord.Interaction, name: str, effect: str, modifier: str):
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

    @app_commands.check(check_admin)
    @app_commands.describe(name="Name of the class", emoji="Emoji for the class", hp="Base HP", attack="Base attack", defense="Base defense", description="Class description")
    async def create_class(self, interaction: discord.Interaction, name: str, emoji: str, hp: int, attack: int, defense: int, description: str):
        await interaction.response.defer()
        if name in CLASS_STATS:
            await interaction.followup.send(f"Class {name} already exists!")
            return
        CLASS_STATS[name] = {
            "emoji": emoji,
            "hp": hp,
            "attack": attack,
            "defense": defense,
            "speed": 15,
            "description": description
        }
        CLASS_ATTACKS[name] = {"name": f"{name} Strike", "damage_range": (15, 25), "effect": f"Standard {name} attack"}
        await interaction.followup.send(f"Created new class {name} with stats: HP {hp}, Attack {attack}, Defense {defense}, Description: {description}")

    @app_commands.describe(user="The user to view stats for (default: yourself)")
    async def stats(self, interaction: discord.Interaction, user: discord.Member = None):
        await interaction.response.defer()
        target = user if user else interaction.user
        profile = self.global_player_profiles.get(target.id, {})
        if not profile:
            await interaction.followup.send(f"{target.mention} has not set up a profile yet!")
            return
        race_effects = ", ".join([f"{effect['name']}: {effect['value']}" for effect in profile.get("race_effects", {}).get("effects", [])]) or "None"
        embed = discord.Embed(title=f"{target.display_name}'s Stats", color=discord.Color.gold())
        embed.add_field(name="Class", value=profile.get("class", "None"), inline=True)
        embed.add_field(name="Attributes", value=", ".join(profile.get("attributes", [])) if profile.get("attributes") else "None", inline=True)
        embed.add_field(name="Race", value=profile.get("race", "None"), inline=True)
        embed.add_field(name="Race Effects", value=race_effects, inline=False)
        embed.add_field(name="Level", value=profile.get("level", 1), inline=True)
        embed.add_field(name="Wins/Losses", value=f"{profile.get('stats', {}).get('wins', 0)}/{profile.get('stats', {}).get('losses', 0)}", inline=True)
        embed.add_field(name="Total Battles", value=profile.get("stats", {}).get("total_battles", 0), inline=True)
        embed.add_field(name="Damage Dealt", value=profile.get("stats", {}).get("total_damage_dealt", 0), inline=True)
        embed.add_field(name="Damage Taken", value=profile.get("stats", {}).get("total_damage_taken", 0), inline=True)
        embed.add_field(name="Critical Hits", value=profile.get("stats", {}).get("critical_hits", 0), inline=True)
        await interaction.followup.send(embed=embed)

    async def on_ready(self):
        print("on_ready event triggered")
        await on_ready(self)

    async def on_message(self, message: discord.Message):
        print(f"on_message event triggered for message {message.id}")
        await on_message(self, message)

    async def on_reaction_add(self, reaction: discord.Reaction, user: discord.User):
        print(f"on_reaction_add event triggered for user {user.name}")
        await on_reaction_add(self, reaction, user)
