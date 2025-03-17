# battle/state.py
from typing import Dict, Any, List
from data.class_types import Player
import random
from data.classes import CLASS_ATTACKS
from data.attributes import ATTRIBUTE_ATTACKS

# Define attack pools for classes, attributes, and neutral options
CLASS_ATTACKS_POOL = {
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

ATTRIBUTE_ATTACKS_POOL = {
    "Fire": [
        {"name": "Fireball", "damage_range": (15, 25), "effect": "A blazing fireball"},
        {"name": "Flame Burst", "damage_range": (10, 20), "effect": "A burst of flames"},
        {"name": "Inferno Strike", "damage_range": (12, 22), "effect": "A fiery slash"}
    ],
    "Water": [
        {"name": "Aqua Shot", "damage_range": (15, 25), "effect": "A precise water shot"},
        {"name": "Wave Crash", "damage_range": (10, 20), "effect": "A crashing wave"},
        {"name": "Hydro Blast", "damage_range": (12, 22), "effect": "A high-pressure blast"}
    ],
    "Air": [
        {"name": "Wind Slash", "damage_range": (15, 25), "effect": "A cutting wind blade"},
        {"name": "Gale Force", "damage_range": (10, 20), "effect": "A forceful gust"},
        {"name": "Air Vortex", "damage_range": (12, 22), "effect": "A spinning air attack"}
    ],
    "Life": [
        {"name": "Healing Pulse", "damage_range": (15, 25), "effect": "A life-infused strike"},
        {"name": "Vital Strike", "damage_range": (10, 20), "effect": "A vitality boost attack"},
        {"name": "Regen Slash", "damage_range": (12, 22), "effect": "A regenerating cut"}
    ]
}

NEUTRAL_ATTACKS = [
    {"name": "Basic Strike", "damage_range": (10, 20), "effect": "A standard neutral attack"},
    {"name": "Power Jab", "damage_range": (8, 18), "effect": "A simple punch"},
    {"name": "Quick Thrust", "damage_range": (9, 19), "effect": "A fast stab"}
]

DEFENSE_OPTIONS = [
    {"name": "Shield Bash", "effect": "Absorbs damage and counters"},
    {"name": "Dodge Roll", "effect": "Evasive maneuver"},
    {"name": "Guard Stance", "effect": "Strengthens defense"}
]

def initialize_battle_state(player1: Player, player2: Player, thread: Any, battlefield: str) -> Dict[str, Any]:
    """Initialize the battle state with two players, a thread, and a battlefield modifier."""
    battle_state = {
        "player1": player1,
        "player2": player2,
        "thread": thread,
        "battlefield": battlefield,
        "turn": player1.user,
        "message": None,
        "reinforce_buff": {},
        "active": True,
        "last_action": None
    }
    return battle_state

def process_attack(attacker: Player, defender: Player, attack_type: str, reinforce_buff: Dict, attack_pool: List = None) -> int:
    """Process an attack and return the damage dealt, using a specific attack pool if provided."""
    if attack_pool and attack_type in [a["name"] for a in attack_pool]:
        attack = next(a for a in attack_pool if a["name"] == attack_type)
        base_damage = random.randint(attack["damage_range"][0], attack["damage_range"][1])
    else:
        base_damage = random.randint(10, 20) if attack_type == "⚔️" else random.randint(15, 25)
    # Apply reinforce buff if present
    if attacker.user.id in reinforce_buff:
        base_damage *= reinforce_buff[attacker.user.id].get("attack_boost", 1.0)
    # Apply defense reduction
    effective_damage = max(0, base_damage - defender.defense)
    defender.take_damage(effective_damage, 0.1)  # 10% dodge chance
    return effective_damage

def get_random_attacks(player: Player) -> List[Dict]:
    """Generate a list of random attacks based on player's class and attributes."""
    attacks = []
    # Add class-specific attack
    if player.class_type in CLASS_ATTACKS_POOL:
        attacks.append(random.choice(CLASS_ATTACKS_POOL[player.class_type]))
    # Add attribute-specific attacks (up to 3)
    for attr in player.attributes:
        if attr in ATTRIBUTE_ATTACKS_POOL and len(attacks) < 3:
            attacks.append(random.choice(ATTRIBUTE_ATTACKS_POOL[attr]))
    # Add neutral attack
    attacks.append(random.choice(NEUTRAL_ATTACKS))
    # Add defense option
    attacks.append(random.choice(DEFENSE_OPTIONS))
    return attacks[:4]  # Limit to 4 options
