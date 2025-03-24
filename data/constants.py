# data/constants.py

CHANNEL_CONFIGS = {
    "class_channel": "🏹・class",
    "battlefield_channel": "🎯・battlefield",
    "stats_channel": "📊・stats",
    "dead_channel": "💀・dead",
    "quest_channel": "📜・quests"
}

# Mastery XP thresholds and titles
MASTERY_LEVELS = [
    (0, "Novice"),
    (100, "Adept"),
    (500, "Expert"),
    (1000, "Master"),
    (2000, "Grand Master")
]

# XP gains
XP_PER_BATTLE_WIN = 10
XP_PER_BATTLE_LOSS = 5
XP_PER_TOURNAMENT_WIN = 50
XP_PER_TOURNAMENT_LOSS = 25
XP_PER_QUEST_COMPLETION = 50
MASTERY_XP_PER_ATTACK = 1
MASTERY_XP_PER_QUEST = 20
COUNTERANCE_XP_PER_ATTACK_RECEIVED = 1
COUNTERANCE_XP_PER_COMBO = 5

# Battle token defaults
DEFAULT_MIN_BATTLE_TOKENS = 3
DEFAULT_MAX_BATTLE_TOKENS = 20
