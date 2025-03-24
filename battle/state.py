# battle/state.py
import random
from data.classes import CLASS_ATTACKS
from data.attributes import ATTRIBUTE_ATTACKS, ATTRIBUTE_INTERACTION_ATTACKS, PRIMARY_ATTRIBUTES, attribute_emojis
from data.constants import XP_PER_BATTLE_WIN, XP_PER_BATTLE_LOSS, MASTERY_XP_PER_ATTACK, COUNTERANCE_XP_PER_ATTACK_RECEIVED, COUNTERANCE_XP_PER_COMBO

NEUTRAL_ATTACKS = [
    {"name": "Basic Strike", "damage_range": (10, 15), "effect": "A standard attack"},
    {"name": "Quick Jab", "damage_range": (8, 12), "effect": "A fast, light hit"},
    {"name": "Heavy Hit", "damage_range": (12, 18), "effect": "A slow but powerful strike"}
]

DEFENSE_OPTIONS = [
    {"name": "Block", "effect": "Reduces damage by 50%", "damage_reduction": 0.5},
    {"name": "Dodge", "effect": "50% chance to avoid damage", "dodge_chance": 0.5},
    {"name": "Counter", "effect": "30% chance to reflect 50% damage", "counter_chance": 0.3, "reflect_percentage": 0.5}
]

COMBO_ATTACKS = {
    ("Fire", "Earth"): {"name": "Lava Eruption", "damage_range": (30, 40), "effect": "A powerful lava attack", "accuracy": 0.9, "self_damage_risk": 0.1},
    ("Fire", "Water"): {"name": "Steam Burst", "damage_range": (20, 30), "effect": "A burst of scalding steam", "accuracy": 0.7, "self_damage_risk": 0.2},
    ("Water", "Ice"): {"name": "Frozen Tide", "damage_range": (25, 35), "effect": "A freezing tidal wave", "accuracy": 0.85, "self_damage_risk": 0.15},
    ("Electric", "Air"): {"name": "Thunderstorm", "damage_range": (25, 35), "effect": "A storm of lightning and wind", "accuracy": 0.85, "self_damage_risk": 0.15},
    ("Earth", "Nature"): {"name": "Forest Quake", "damage_range": (25, 35), "effect": "A quaking forest attack", "accuracy": 0.85, "self_damage_risk": 0.15},
    ("Light", "Life"): {"name": "Holy Restoration", "damage_range": (20, 30), "effect": "A restorative light attack", "accuracy": 0.8, "self_damage_risk": 0.1},
    ("Shadow", "Death"): {"name": "Necrotic Abyss", "damage_range": (25, 35), "effect": "A dark necrotic strike", "accuracy": 0.85, "self_damage_risk": 0.15}
}

def initialize_battle_state(player1, player2, thread, battlefield, is_bot_fight=False):
    return {
        "player1": player1,
        "player2": player2,
        "thread": thread,
        "battlefield": battlefield,
        "turn": player1.user,
        "message": None,
        "active": True,
        "reinforcements": [],
        "is_bot_fight": is_bot_fight,
        "last_action": None
    }

def get_random_attacks(player):
    attacks = []
    # Class attack
    class_attacks = CLASS_ATTACKS.get(player.class_type, [])
    if class_attacks:
        attacks.append(random.choice(class_attacks))
    # Attribute attacks
    for attr in player.attributes:
        attr_attacks = ATTRIBUTE_ATTACKS.get(attr, [])
        if attr_attacks:
            attacks.append(random.choice(attr_attacks))
    # Basic attack
    attacks.append(random.choice(NEUTRAL_ATTACKS))
    # Defense option
    attacks.append(random.choice(DEFENSE_OPTIONS))
    return attacks

def process_attack(attacker, defender, attack_name, reinforce_buff, attacks, battlefield):
    attack = next((a for a in attacks if a["name"] == attack_name), None)
    if not attack:
        return 0
    damage = 0
    if "damage_range" in attack:
        damage = random.randint(attack["damage_range"][0], attack["damage_range"][1])
        # Apply battlefield modifiers
        from data.battlefields import BATTLEFIELD_MODIFIERS
        battlefield_modifiers = BATTLEFIELD_MODIFIERS.get(battlefield, {})
        for attr, modifier in battlefield_modifiers.items():
            if attr in attack_name.lower() and modifier["type"] == "boost":
                damage *= modifier["value"]
            elif attr in attack_name.lower() and modifier["type"] == "nerf":
                damage *= modifier["value"]
        # Apply counterance XP reduction
        counterance_key = f"attr_{next((attr for attr in PRIMARY_ATTRIBUTES if attr.lower() in attack_name.lower()), None)}"
        if counterance_key:
            counterance_xp = defender.global_player_profiles[defender.user.id]["counterance_xp"].get(counterance_key, 0)
            reduction = min(counterance_xp / 1000, 0.5)  # Max 50% reduction
            damage *= (1 - reduction)
        # Apply critical hit
        if random.random() < 0.1:  # 10% chance
            damage *= 1.5
            attacker.stats["critical_hits"] += 1
            attacker.global_player_profiles[attacker.user.id]["stats"]["critical_hits"] += 1
    defender.hp -= damage
    attacker.stats["total_damage_dealt"] += damage
    attacker.global_player_profiles[attacker.user.id]["stats"]["total_damage_dealt"] += damage
    defender.stats["total_damage_taken"] += damage
    defender.global_player_profiles[defender.user.id]["stats"]["total_damage_taken"] += damage
    # Update counterance XP
    counterance_key = f"attr_{next((attr for attr in PRIMARY_ATTRIBUTES if attr.lower() in attack_name.lower()), None)}"
    if counterance_key:
        defender.global_player_profiles[defender.user.id]["counterance_xp"][counterance_key] = defender.global_player_profiles[defender.user.id]["counterance_xp"].get(counterance_key, 0) + COUNTERANCE_XP_PER_ATTACK_RECEIVED
    # Update mastery XP
    mastery_key = f"attr_{next((attr for attr in PRIMARY_ATTRIBUTES if attr.lower() in attack_name.lower()), None)}"
    if mastery_key:
        attacker.global_player_profiles[attacker.user.id]["attribute_mastery_xp"][mastery_key.split("_")[1]] = attacker.global_player_profiles[attacker.user.id]["attribute_mastery_xp"].get(mastery_key.split("_")[1], 0) + MASTERY_XP_PER_ATTACK
    if attack_name in [a["name"] for a in CLASS_ATTACKS.get(attacker.class_type, [])]:
        attacker.global_player_profiles[attacker.user.id]["class_mastery_xp"] += MASTERY_XP_PER_ATTACK
    return damage

def process_combo_attack(attacker, defender, combo_attributes, teamwork_xp, battlefield):
    combo_key = tuple(sorted(combo_attributes))
    combo_attack = COMBO_ATTACKS.get(combo_key, {"name": f"{combo_attributes[0]} {combo_attributes[1]} Combo", "damage_range": (20, 30), "effect": "A combined elemental attack", "accuracy": 0.75, "self_damage_risk": 0.15})
    damage = random.randint(combo_attack["damage_range"][0], combo_attack["damage_range"][1])
    # Apply accuracy based on teamwork XP
    accuracy = combo_attack["accuracy"] + min(teamwork_xp / 1000, 0.2)  # Max 20% accuracy boost
    if random.random() > accuracy:
        damage = 0
    # Apply self-damage risk based on teamwork XP
    self_damage_risk = combo_attack["self_damage_risk"] - min(teamwork_xp / 1000, 0.1)  # Max 10% risk reduction
    if random.random() < self_damage_risk:
        self_damage = damage // 2
        attacker.hp -= self_damage
        attacker.stats["total_damage_taken"] += self_damage
        attacker.global_player_profiles[attacker.user.id]["stats"]["total_damage_taken"] += self_damage
    # Apply battlefield modifiers
    from data.battlefields import BATTLEFIELD_MODIFIERS
    battlefield_modifiers = BATTLEFIELD_MODIFIERS.get(battlefield, {})
    for attr, modifier in battlefield_modifiers.items():
        if attr in combo_attributes and modifier["type"] == "boost":
            damage *= modifier["value"]
        elif attr in combo_attributes and modifier["type"] == "nerf":
            damage *= modifier["value"]
    # Apply counterance XP reduction
    for attr in combo_attributes:
        counterance_key = f"attr_{attr}"
        counterance_xp = defender.global_player_profiles[defender.user.id]["counterance_xp"].get(counterance_key, 0)
        reduction = min(counterance_xp / 1000, 0.5)  # Max 50% reduction
        damage *= (1 - reduction)
    # Apply critical hit
    if random.random() < 0.1:  # 10% chance
        damage *= 1.5
        attacker.stats["critical_hits"] += 1
        attacker.global_player_profiles[attacker.user.id]["stats"]["critical_hits"] += 1
    defender.hp -= damage
    attacker.stats["total_damage_dealt"] += damage
    attacker.global_player_profiles[attacker.user.id]["stats"]["total_damage_dealt"] += damage
    defender.stats["total_damage_taken"] += damage
    defender.global_player_profiles[defender.user.id]["stats"]["total_damage_taken"] += damage
    # Update counterance XP
    for attr in combo_attributes:
        counterance_key = f"attr_{attr}"
        defender.global_player_profiles[defender.user.id]["counterance_xp"][counterance_key] = defender.global_player_profiles[defender.user.id]["counterance_xp"].get(counterance_key, 0) + COUNTERANCE_XP_PER_COMBO
    # Update mastery XP
    for attr in combo_attributes:
        attacker.global_player_profiles[attacker.user.id]["attribute_mastery_xp"][attr] = attacker.global_player_profiles[attacker.user.id]["attribute_mastery_xp"].get(attr, 0) + MASTERY_XP_PER_ATTACK
    return damage, combo_attack["name"]
