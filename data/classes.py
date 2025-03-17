# data/classes.py

CLASS_STATS = {
    "Winged Creature": {
        "emoji": "🕊️",
        "hp": 80,
        "attack": 25,
        "defense": 10,
        "speed": 20,
        "description": "A swift and agile creature of the skies, excelling in speed and attack."
    },
    "Ground Creature": {
        "emoji": "🦁",
        "hp": 100,
        "attack": 20,
        "defense": 15,
        "speed": 10,
        "description": "A sturdy beast of the land, strong in HP and defense."
    },
    "Aquatic Creature": {
        "emoji": "🐙",
        "hp": 90,
        "attack": 15,
        "defense": 12,
        "speed": 15,
        "description": "A versatile denizen of the deep, balanced with a slight speed advantage."
    }
}

CLASS_ATTACKS = {
    "Winged Creature": {"name": "Sky Dive", "damage_range": (20, 30), "effect": "Swoops down with high speed, increasing critical chance by 10%"},
    "Ground Creature": {"name": "Earth Stomp", "damage_range": (15, 25), "effect": "Shakes the ground, reducing target dodge chance by 10%"},
    "Aquatic Creature": {"name": "Wave Crash", "damage_range": (18, 28), "effect": "Crashes with a wave, reducing target speed by 5"}
}
