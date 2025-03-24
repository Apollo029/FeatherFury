# data/classes.py

# Define class statistics with emoji, stats, and description
CLASS_STATS = {
    "Winged Creature": {
        "emoji": "🕊️",
        "hp": 80,
        "attack": 20,
        "defense": 15,
        "speed": 25,
        "description": "A swift and agile creature of the skies."
    },
    "Aquatic Creature": {
        "emoji": "🐙",
        "hp": 90,
        "attack": 18,
        "defense": 20,
        "speed": 15,
        "description": "A resilient creature from the depths."
    },
    "Ground Creature": {
        "emoji": "🦁",
        "hp": 100,
        "attack": 22,
        "defense": 18,
        "speed": 12,
        "description": "A sturdy creature of the earth."
    }
}

# Define class-specific attacks
CLASS_ATTACKS = {
    "Winged Creature": [
        {"name": "Aerial Slash", "damage_range": (15, 25), "effect": "A swift air-based strike"},
        {"name": "Wind Gust", "damage_range": (10, 20), "effect": "A gust that disrupts the enemy"},
        {"name": "Feather Storm", "damage_range": (12, 22), "effect": "A flurry of feather attacks"}
    ],
    "Aquatic Creature": [
        {"name": "Water Jet", "damage_range": (15, 25), "effect": "A powerful water blast"},
        {"name": "Tidal Wave", "damage_range": (10, 20), "effect": "A sweeping water attack"},
        {"name": "Bubble Barrage", "damage_range": (12, 22), "effect": "A barrage of water bubbles"}
    ],
    "Ground Creature": [
        {"name": "Earth Smash", "damage_range": (15, 25), "effect": "A crushing earth strike"},
        {"name": "Rock Throw", "damage_range": (10, 20), "effect": "A hurled rock attack"},
        {"name": "Quake Stomp", "damage_range": (12, 22), "effect": "A ground-shaking stomp"}
    ]
}

# Define announcements for class selection
CLASS_ANNOUNCEMENTS = {
    "Winged Creature": [
        "Behold! {player} has ascended as a {class_name}!",
        "{player} soars into battle as a {class_name}!",
        "The skies welcome {player} as a {class_name}!"
    ],
    "Aquatic Creature": [
        "Dive in! {player} emerges as a {class_name}!",
        "{player} makes waves as a {class_name}!",
        "The depths embrace {player} as a {class_name}!"
    ],
    "Ground Creature": [
        "Feel the earth shake! {player} stands as a {class_name}!",
        "{player} roars into battle as a {class_name}!",
        "The ground trembles as {player} becomes a {class_name}!"
    ]
}
