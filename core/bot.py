# core/bot.py
import discord
from discord import app_commands
import asyncio
from core.events import on_ready, on_message, on_reaction_add
from data.constants import CHANNEL_CONFIGS
from data.attributes import PRIMARY_ATTRIBUTES, attribute_emojis

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
        self.class_selection_message = {}
        self.attribute_selection_message = {}
        self.race_selection_message = {}
        self.stats_message_ids = {}
        self.active_battles = {}
        self.battle_counter = 0
        self.tournament_active = False
        self.tournament_bracket = {}
        self.tournament_winner = None
        self.current_quarter = (discord.utils.utcnow().month - 1) // 3 + 1
        self.reaction_processed = {}
        print("Bot attributes initialized")

        # Define commands here
        @self.tree.command(name="attack", description="Start a battle with another user or bot")
        @app_commands.describe(opponent="The user or bot to battle", battlefield="The battlefield type")
        @app_commands.choices(battlefield=[
            app_commands.Choice(name="Random", value="Random"),
            app_commands.Choice(name="Fire", value="Fire"),
            app_commands.Choice(name="Water", value="Water"),
            app_commands.Choice(name="Ice", value="Ice"),
            app_commands.Choice(name="Electric", value="Electric"),
            app_commands.Choice(name="Earth", value="Earth"),
            app_commands.Choice(name="Nature", value="Nature"),
            app_commands.Choice(name="Metal", value="Metal"),
            app_commands.Choice(name="Air", value="Air"),
            app_commands.Choice(name="Light", value="Light"),
            app_commands.Choice(name="Shadow", value="Shadow"),
            app_commands.Choice(name="Life", value="Life"),
            app_commands.Choice(name="Death", value="Death")
        ])
        async def attack(interaction: discord.Interaction, opponent: discord.Member, battlefield: str = "Random"):
            await self.attack(interaction, opponent, battlefield)

        @self.tree.command(name="reinforce", description="Call for reinforcements in an active battle")
        async def reinforce(interaction: discord.Interaction):
            await self.reinforce(interaction)

        @self.tree.command(name="enter_race", description="Enter a race with a custom name and color")
        @app_commands.describe(name="The name of your race", color="The color of your race (e.g., red, #000000, 000000)")
        async def enter_race(interaction: discord.Interaction, name: str, color: str):
            await self.enter_race(interaction, name, color)

        @self.tree.command(name="stats", description="View your stats or another user's stats")
        @app_commands.describe(user="The user to view stats for (default: yourself)")
        async def stats(interaction: discord.Interaction, user: discord.Member = None):
            await self.stats(interaction, user)

        @self.tree.command(name="counterance_stats", description="View your counterance stats (hidden stats)")
        async def counterance_stats(interaction: discord.Interaction):
            await self.counterance_stats(interaction)

        @self.tree.command(name="config", description="Configure server settings (admin only)")
        @app_commands.check(self.check_admin)
        @app_commands.describe(min_tokens="Minimum battle tokens per week", max_tokens="Maximum battle tokens allowed")
        async def config(interaction: discord.Interaction, min_tokens: int = None, max_tokens: int = None):
            await self.config(interaction, min_tokens, max_tokens)

    async def setup_hook(self):
        print("Syncing command tree...")
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

@app_commands.command(name="attack", description="Start a battle with another user or bot")
@app_commands.describe(opponent="The user or bot to battle", battlefield="The battlefield type")
@app_commands.choices(battlefield=[
    app_commands.Choice(name="Random", value="Random"),
    app_commands.Choice(name="Fire", value="Fire"),
    app_commands.Choice(name="Water", value="Water"),
    app_commands.Choice(name="Ice", value="Ice"),
    app_commands.Choice(name="Electric", value="Electric"),
    app_commands.Choice(name="Earth", value="Earth"),
    app_commands.Choice(name="Nature", value="Nature"),
    app_commands.Choice(name="Metal", value="Metal"),
    app_commands.Choice(name="Air", value="Air"),
    app_commands.Choice(name="Light", value="Light"),
    app_commands.Choice(name="Shadow", value="Shadow"),
    app_commands.Choice(name="Life", value="Life"),
    app_commands.Choice(name="Death", value="Death")
])
async def attack(self, interaction: discord.Interaction, opponent: discord.Member, battlefield: str = "Random"):
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

    # Check if opponent is FeatherFury and user is not a Grand Master
    if opponent.id == self.user.id:  # FeatherFury
        user_profile = self.global_player_profiles[user.id]
        required_mastery = ["Grand Master"]
        is_grand_master = (
            user_profile.get("class_mastery_title", "Novice") in required_mastery and
            all(user_profile.get(f"{attr}_mastery_title", "Novice") in required_mastery for attr in user_profile.get("attributes", []))
        )
        if not is_grand_master:
            await interaction.followup.send(f"{user.mention}, you are not worthy to challenge {opponent.mention}! You must be a Grand Master in your class and all attributes.")
            # Simulate instant kill
            user_profile["stats"]["losses"] += 1
            user_profile["stats"]["losses_to_bots"] += 1
            opponent_profile = self.global_player_profiles[opponent.id]
            opponent_profile["stats"]["wins"] += 1
            opponent_profile["stats"]["bots_beaten"] += 1
            from utils.roles import assign_dead_role
            await assign_dead_role(guild, user)
            from core.events import update_stats_embed
            await update_stats_embed(self, guild, user.id)
            await update_stats_embed(self, guild, opponent.id)
            return

    # Handle battle tokens
    from data.battlefields import BATTLEFIELD_MODIFIERS
    user_profile = self.global_player_profiles[user.id]
    server_tokens = user_profile.setdefault("battle_tokens", {}).setdefault(str(guild.id), 3)
    if battlefield == "Random":
        battlefield = random.choice(list(BATTLEFIELD_MODIFIERS.keys()))
        await interaction.followup.send(f"{user.mention}, you selected Random battlefield. Chosen: {battlefield}.")
    else:
        if battlefield not in BATTLEFIELD_MODIFIERS:
            await interaction.followup.send(f"Invalid battlefield type {battlefield}. Available: {', '.join(BATTLEFIELD_MODIFIERS.keys())}")
            return
        if server_tokens < 1:
            battlefield = random.choice(list(BATTLEFIELD_MODIFIERS.keys()))
            await interaction.followup.send(f"{user.mention}, you have no battle tokens! Randomizing battlefield to {battlefield}.")
        else:
            user_profile["battle_tokens"][str(guild.id)] -= 1
            await interaction.followup.send(f"{user.mention} used a battle token to select {battlefield}. Tokens remaining: {user_profile['battle_tokens'][str(guild.id)]}")

    # Start the battle
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
    battle_id = f"battle_{self.battle_counter}_{int(discord.utils.utcnow().timestamp())}"
    from data.class_types import Player
    player1 = Player(user, self.global_player_profiles[user.id]["class"], self.global_player_profiles[user.id]["attributes"], self.global_player_profiles[user.id]["level"], self.global_player_profiles[user.id]["race"], self.global_player_profiles[user.id]["race_effects"])
    player2 = Player(opponent, self.global_player_profiles[opponent.id]["class"], self.global_player_profiles[opponent.id]["attributes"], self.global_player_profiles[opponent.id]["level"], self.global_player_profiles[opponent.id]["race"], self.global_player_profiles[opponent.id]["race_effects"])
    print(f"Player1 stats: hp={player1.hp}/{player1.max_hp}, attack={player1.attack}, defense={player1.defense}, speed={player1.speed}")
    print(f"Player2 stats: hp={player2.hp}/{player2.max_hp}, attack={player2.attack}, defense={player2.defense}, speed={player2.speed}")
    from battle.state import initialize_battle_state
    self.active_battles[battle_id] = initialize_battle_state(player1, player2, thread, battlefield, is_bot_fight=opponent.bot)
    await self.active_battles[battle_id]["thread"].send(f"Battle started between {user.mention} and {opponent.mention} in {self.active_battles[battle_id]['battlefield']}!\n{BATTLEFIELD_DESCRIPTIONS[self.active_battles[battle_id]['battlefield']]}")
    turn_message = await self.active_battles[battle_id]["thread"].send(f"{user.mention}'s turn! React with an attribute, ⚔️, or 🛡️ to act.")
    for attr in player1.attributes:
        if attr in PRIMARY_ATTRIBUTES:
            emoji = attribute_emojis.get(attr, "❓")
            await turn_message.add_reaction(emoji)
    await turn_message.add_reaction("⚔️")
    await turn_message.add_reaction("🛡️")
    self.active_battles[battle_id]["message"] = turn_message
    self.reaction_processed[battle_id] = set()

    # Placeholder for battle resolution (simplified for now)
    await asyncio.sleep(5)  # Simulate battle duration
    winner = random.choice([player1, player2])
    loser = player2 if winner == player1 else player1
    winner_profile = self.global_player_profiles[winner.user.id]
    loser_profile = self.global_player_profiles[loser.user.id]
    winner_profile["stats"]["wins"] += 1
    if loser.user.bot:
        winner_profile["stats"]["bots_beaten"] += 1
    loser_profile["stats"]["losses"] += 1
    if winner.user.bot:
        loser_profile["stats"]["losses_to_bots"] += 1
    # Check if winner beat FeatherFury
    if loser.user.id == self.user.id:  # FeatherFury was defeated
        featherfury_profile = self.global_player_profiles[loser.user.id]
        featherfury_profile.setdefault("has_been_beaten", {})[str(winner.user.id)] = True
        await battle["thread"].send(f"{winner.user.mention} has defeated {loser.user.mention}! You have proven your worth and can now call upon {loser.user.mention} as a reinforcement.")
    else:
        await battle["thread"].send(f"{winner.user.mention} has defeated {loser.user.mention}!")
    battle["active"] = False
    from core.events import update_stats_embed
    await update_stats_embed(self, guild, winner.user.id)
    await update_stats_embed(self, guild, loser.user.id)

@app_commands.command(name="reinforce", description="Call for reinforcements in an active battle")
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
    if battle["is_bot_fight"]:
        await interaction.followup.send(f"{user.mention}, reinforcements are not allowed in bot fights!")
        return
    player = battle["player1"] if user == battle["player1"].user else battle["player2"]
    if player.hp > player.max_hp * 0.1:
        await interaction.followup.send(f"{user.mention}, your HP must be below 10% to call for reinforcements!")
        return
    if len(battle.get("reinforcements", [])) >= 2:
        await interaction.followup.send(f"{user.mention}, you already have the maximum number of reinforcements (2)!")
        return

    # Check if calling FeatherFury
    guild = interaction.guild
    featherfury = guild.get_member(self.user.id)
    if featherfury in battle.get("reinforcements", []):
        await interaction.followup.send(f"{user.mention}, you have already called {featherfury.mention} as a reinforcement!")
        return

    # Check if user has beaten FeatherFury
    featherfury_profile = self.global_player_profiles.get(featherfury.id, {})
    has_beaten_featherfury = featherfury_profile.get("has_been_beaten", {}).get(str(user.id), False)
    if not has_beaten_featherfury:
        await interaction.followup.send(f"{user.mention}, you dare call upon {featherfury.mention} without defeating him? He strikes you down in one blow!")
        player.hp = 0
        player.alive = False
        user_profile = self.global_player_profiles[user.id]
        user_profile["stats"]["losses"] += 1
        user_profile["stats"]["losses_to_bots"] += 1
        from utils.roles import assign_dead_role
        await assign_dead_role(guild, user)
        from core.events import update_stats_embed
        await update_stats_embed(self, guild, user.id)
        battle["active"] = False
        await battle["thread"].send(f"{user.mention} has been defeated by {featherfury.mention}!")
        return

    # Add FeatherFury as a reinforcement
    battle["reinforcements"].append(featherfury)
    await interaction.followup.send(f"{featherfury.mention} joins {user.mention} in battle, ready to fight alongside you!")

    @app_commands.command(name="enter_race", description="Enter a race with a custom name and color")
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
        from data.class_types import generate_race_effects
        race_effects = await generate_race_effects(name, color, class_type=class_type, attributes=attributes, is_bot=False)
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
                "losses_to_bots": 0,
                "monthly_trophies": 0,
                "quarterly_trophies": 0
            },
            "level": profile.get("level", 1),
            "xp": profile.get("xp", 0),
            "teamwork_xp": profile.get("teamwork_xp", 0),
            "class_mastery_xp": profile.get("class_mastery_xp", 0),
            "class_mastery_title": profile.get("class_mastery_title", "Novice"),
            "attribute_mastery_xp": profile.get("attribute_mastery_xp", {}),
            "attribute_mastery_titles": profile.get("attribute_mastery_titles", {}),
            "counterance_xp": profile.get("counterance_xp", {}),
            "battle_tokens": profile.get("battle_tokens", {}),
            "race_effects": race_effects,
            "race_color": color
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
            self.global_player_profiles[user.id]["race_color"] = hex_color
            confirmation = await interaction.followup.send(f"Successfully completed /EnterRace for {user.display_name} with race {name} and effects {race_effects['effects']}")
            await asyncio.sleep(10)
            await confirmation.delete()
            from core.events import update_stats_embed
            await update_stats_embed(self, guild, user.id)
        except discord.HTTPException as e:
            await interaction.followup.send(f"Failed to create role for race {name}: {e}")

    @app_commands.command(name="stats", description="View your stats or another user's stats")
    @app_commands.describe(user="The user to view stats for (default: yourself)")
    async def stats(self, interaction: discord.Interaction, user: discord.Member = None):
        await interaction.response.defer()
        target = user if user else interaction.user
        profile = self.global_player_profiles.get(target.id, {})
        if not profile:
            await interaction.followup.send(f"{target.mention} has not set up a profile yet!")
            return
        race_effects = profile.get("race_effects", {}).get("effects", [])
        race_effects_display = "\n".join([
            f"{effect['name']}: {effect['value']}" + 
            (f" (Weakness: {effect['weakness']}, Strength: {effect['strength']})" if effect.get("type") == "dual" else "")
            for effect in race_effects
        ]) or "None"
        race_color = profile.get("race_color", "#FFD700")
        try:
            embed_color = discord.Color.from_str(race_color)
        except ValueError:
            embed_color = discord.Color.gold()
        embed = discord.Embed(title=f"{target.display_name}'s Stats", color=embed_color)
        embed.add_field(name="Class", value=profile.get("class", "None"), inline=True)
        embed.add_field(name="Attributes", value=", ".join(profile.get("attributes", [])) if profile.get("attributes") else "None", inline=True)
        embed.add_field(name="Race", value=profile.get("race", "None"), inline=True)
        embed.add_field(name="Race Effects", value=race_effects_display, inline=False)
        embed.add_field(name="Level", value=profile.get("level", 1), inline=True)
        wins = profile.get("stats", {}).get("wins", 0)
        bots_beaten = profile.get("stats", {}).get("bots_beaten", 0)
        embed.add_field(name="Wins (Players/Bots)", value=f"{wins}/{bots_beaten}", inline=True)
        total_battles = profile.get("stats", {}).get("total_battles", 0)
        embed.add_field(name="Total Battles", value=total_battles, inline=True)
        damage_dealt = profile.get("stats", {}).get("total_damage_dealt", 0)
        embed.add_field(name="Damage Dealt", value=damage_dealt, inline=True)
        damage_taken = profile.get("stats", {}).get("total_damage_taken", 0)
        embed.add_field(name="Damage Taken", value=damage_taken, inline=True)
        critical_hits = profile.get("stats", {}).get("critical_hits", 0)
        embed.add_field(name="Critical Hits", value=critical_hits, inline=True)
        monthly_trophies = profile.get("stats", {}).get("monthly_trophies", 0)
        quarterly_trophies = profile.get("stats", {}).get("quarterly_trophies", 0)
        embed.add_field(name="Trophies (Monthly/Quarterly)", value=f"{monthly_trophies}/{quarterly_trophies}", inline=True)
        battle_tokens = profile.get("battle_tokens", {}).get(str(interaction.guild.id), 3)
        embed.add_field(name="Battle Tokens", value=battle_tokens, inline=True)
        xp = profile.get("xp", 0)
        embed.add_field(name="XP", value=xp, inline=True)
        teamwork_xp = profile.get("teamwork_xp", 0)
        embed.add_field(name="Teamwork XP", value=teamwork_xp, inline=True)
        class_mastery = f"{profile.get('class_mastery_title', 'Novice')} ({profile.get('class_mastery_xp', 0)} XP)"
        embed.add_field(name=f"{profile.get('class', 'None')} Mastery", value=class_mastery, inline=True)
        for attr in profile.get("attributes", []):
            attr_mastery = f"{profile.get('attribute_mastery_titles', {}).get(attr, 'Novice')} ({profile.get('attribute_mastery_xp', {}).get(attr, 0)} XP)"
            embed.add_field(name=f"{attr} Mastery", value=attr_mastery, inline=True)
        from core.events import update_stats_embed
        await update_stats_embed(self, interaction.guild, target.id, embed=embed)
        await interaction.followup.send(embed=embed)

    @app_commands.command(name="counterance_stats", description="View your counterance stats (hidden stats)")
    async def counterance_stats(self, interaction: discord.Interaction):
        await interaction.response.defer()
        user = interaction.user
        profile = self.global_player_profiles.get(user.id, {})
        if not profile:
            await interaction.followup.send(f"{user.mention}, you have not set up a profile yet!")
            return
        embed = discord.Embed(title=f"{user.display_name}'s Counterance Stats", color=discord.Color.purple())
        counterance_xp = profile.get("counterance_xp", {})
        for class_name in CLASS_STATS.keys():
            xp = counterance_xp.get(f"class_{class_name}", 0)
            embed.add_field(name=f"{class_name} Counterance", value=f"{xp} XP", inline=True)
        for attr in PRIMARY_ATTRIBUTES:
            xp = counterance_xp.get(f"attr_{attr}", 0)
            embed.add_field(name=f"{attr} Counterance", value=f"{xp} XP", inline=True)
        message = await interaction.followup.send(embed=embed)
        await asyncio.sleep(20)
        await message.delete()

    @app_commands.command(name="config", description="Configure server settings (admin only)")
    @app_commands.check(check_admin)
    @app_commands.describe(min_tokens="Minimum battle tokens per week", max_tokens="Maximum battle tokens allowed")
    async def config(self, interaction: discord.Interaction, min_tokens: int = None, max_tokens: int = None):
        await interaction.response.defer()
        guild = interaction.guild
        from utils.config import update_server_config, get_server_config
        config = get_server_config(guild.id)
        if min_tokens is not None:
            config["min_battle_tokens"] = min_tokens
        if max_tokens is not None:
            config["max_battle_tokens"] = max_tokens
        update_server_config(guild.id, config)
        await interaction.followup.send(f"Updated server config: Min Tokens = {config['min_battle_tokens']}, Max Tokens = {config['max_battle_tokens']}")

    async def on_ready(self):
        print("on_ready event triggered")
        await on_ready(self)

    async def on_message(self, message: discord.Message):
        print(f"on_message event triggered for message {message.id}")
        await on_message(self, message)

    async def on_reaction_add(self, reaction: discord.Reaction, user: discord.User):
        print(f"on_reaction_add event triggered for user {user.name}")
        await on_reaction_add(self, reaction, user)
