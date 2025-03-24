# data/class_types.py
from typing import List, Dict
from data.classes import CLASS_STATS
import random

# Define effect pools for attributes
ATTRIBUTE_EFFECTS = {
    "Fire": {
        "buffs": [
            {"name": "Blaze Boost", "value": "+15% Fire Damage", "type": "normal"},
            {"name": "Heat Wave", "value": "+10 Attack", "type": "normal"},
            {"name": "Flame Aura", "value": "+5% Burn Chance", "type": "normal"},
        ],
        "debuffs": [
            {"name": "Burnout", "value": "-5 HP", "type": "normal"},
            {"name": "Overheat", "value": "-10% Attack", "type": "normal"},
            {"name": "Ashen Skin", "value": "-5 Defense", "type": "normal"},
        ],
        "dual_buffs": [
            {"name": "Inferno Rage", "value": "+30% Fire Damage, Burn Effect", "type": "dual", "weakness": "Water", "strength": "Fire"},
            {"name": "Firestorm", "value": "+35% Fire Damage", "type": "dual", "weakness": "Water", "strength": "Fire"},
        ]
    },
    "Water": {
        "buffs": [
            {"name": "Current Flow", "value": "+10% Healing", "type": "normal"},
            {"name": "Wave Rider", "value": "+10 Speed", "type": "normal"},
            {"name": "Aqua Barrier", "value": "+15 Defense", "type": "normal"},
        ],
        "debuffs": [
            {"name": "Drowning", "value": "-5 HP", "type": "normal"},
            {"name": "Slow Current", "value": "-10% Speed", "type": "normal"},
            {"name": "Wet Armor", "value": "-5 Defense", "type": "normal"},
        ],
        "dual_buffs": [
            {"name": "Tsunami Wave", "value": "+25% Water Damage", "type": "dual", "weakness": "Fire", "strength": "Water"},
            {"name": "Flood Tide", "value": "+30% Water Damage", "type": "dual", "weakness": "Fire", "strength": "Water"},
        ]
    },
    "Ice": {
        "buffs": [
            {"name": "Frost Shield", "value": "+15 Defense", "type": "normal"},
            {"name": "Chill Touch", "value": "+10 Attack", "type": "normal"},
            {"name": "Ice Armor", "value": "+5% Damage Reduction", "type": "normal"},
        ],
        "debuffs": [
            {"name": "Frozen Limbs", "value": "-5 Speed", "type": "normal"},
            {"name": "Cold Snap", "value": "-10% Attack", "type": "normal"},
            {"name": "Icy Skin", "value": "-5 HP", "type": "normal"},
        ],
        "dual_buffs": [
            {"name": "Glacial Burst", "value": "+20% Ice Damage, Freeze Effect", "type": "dual", "weakness": "Fire", "strength": "Ice"},
            {"name": "Arctic Blast", "value": "+25% Ice Damage", "type": "dual", "weakness": "Fire", "strength": "Ice"},
        ]
    },
    # Add more attributes as needed
}

class Player:
    def __init__(self, user, class_type: str, attributes: List[str], level: int, race: str, race_effects: Dict = None):
        self.user = user
        self.class_type = class_type
        self.attributes = attributes
        self.level = level
        self.race = race
        self.race_effects = race_effects or {"effects": [], "power_index": 0}
        self.max_hp = self._set_hp()
        self.hp = self.max_hp
        self.attack = self._set_attack()
        self.defense = self._set_defense()
        self.speed = self._set_speed()
        self.alive = True
        self.stats = {
            "wins": 0,
            "losses": 0,
            "total_battles": 0,
            "total_damage_dealt": 0,
            "total_damage_taken": 0,
            "critical_hits": 0,
            "critical_wins": 0,
            "bots_beaten": 0,
            "losses_to_bots": 0
        }

    def _set_hp(self):
        base_hp = CLASS_STATS.get(self.class_type, {"hp": 80})["hp"]
        for effect in self.race_effects.get("effects", []):
            if effect["type"] == "normal" and "HP" in effect["value"]:
                value = int(effect["value"].split("+")[1].split()[0]) if "+" in effect["value"] else -int(effect["value"].split("-")[1].split()[0])
                base_hp += value
            elif effect["type"] == "dual" and effect["name"] in ["Balanced Power", "Harmonic Boost"]:
                base_hp += 20
        return base_hp + (self.level - 1) * 5

    def _set_attack(self):
        base_attack = CLASS_STATS.get(self.class_type, {"attack": 20})["attack"]
        for effect in self.race_effects.get("effects", []):
            if effect["type"] == "normal" and "Attack" in effect["value"]:
                value = int(effect["value"].split("+")[1].split()[0]) if "+" in effect["value"] else -int(effect["value"].split("-")[1].split()[0])
                base_attack += value
            elif effect["type"] == "dual" and "%" in effect["value"]:
                percentage = int(effect["value"].split("+")[1].split("%")[0])
                base_attack *= (1 + percentage / 100)
                if "strength" in effect and effect["strength"] in self.attributes:
                    base_attack *= 1.2  # 20% boost
                if "weakness" in effect and effect["weakness"] in self.attributes:
                    base_attack *= 0.8  # 20% reduction
        return base_attack + (self.level - 1) * 2

    def _set_defense(self):
        base_defense = CLASS_STATS.get(self.class_type, {"defense": 15})["defense"]
        for effect in self.race_effects.get("effects", []):
            if effect["type"] == "normal" and "Defense" in effect["value"]:
                value = int(effect["value"].split("+")[1].split()[0]) if "+" in effect["value"] else -int(effect["value"].split("-")[1].split()[0])
                base_defense += value
            elif effect["type"] == "dual" and effect["name"] in ["Harmonic Boost"]:
                base_defense += 20
        return base_defense + (self.level - 1) * 1

    def _set_speed(self):
        base_speed = CLASS_STATS.get(self.class_type, {"speed": 15})["speed"]
        for effect in self.race_effects.get("effects", []):
            if effect["type"] == "normal" and "Speed" in effect["value"]:
                value = int(effect["value"].split("+")[1].split()[0]) if "+" in effect["value"] else -int(effect["value"].split("-")[1].split()[0])
                base_speed += value
        return base_speed + (self.level - 1) * 1

    def take_damage(self, damage: int, dodge_chance: float = 0.1):
        if random.random() < dodge_chance:
            print(f"{self.user.name} dodged the attack!")
            return 0
        effective_damage = max(0, damage - self.defense)
        self.hp = max(0, self.hp - effective_damage)
        self.stats["total_damage_taken"] += effective_damage
        if self.hp <= 0:
            self.alive = False
        return effective_damage

    def heal(self, amount: int):
        self.hp = min(self.max_hp, self.hp + amount)

def generate_race_effects(race_name: str, color: str, class_type: str = None, attributes: List[str] = None) -> Dict:
    """Generate race effects based on attributes."""
    effects = []
    power_index = 0

    # Select up to 2 effects from attributes (buffs, debuffs, dual buffs)
    if attributes:
        attr_effects = []
        for attr in attributes:
            if attr in ATTRIBUTE_EFFECTS:
                attr_pools = [ATTRIBUTE_EFFECTS[attr]["buffs"], ATTRIBUTE_EFFECTS[attr]["debuffs"], ATTRIBUTE_EFFECTS[attr]["dual_buffs"]]
                all_attr_effects = [effect for pool in attr_pools for effect in pool]
                if all_attr_effects:
                    attr_effects.append(random.choice(all_attr_effects))
        if len(attr_effects) > 1:
            selected_attr_effects = random.sample(attr_effects, 2)
        elif attr_effects:
            selected_attr_effects = [attr_effects[0]]
        else:
            selected_attr_effects = []
        effects.extend(selected_attr_effects)
        power_index += 5 if any(e["type"] == "normal" for e in selected_attr_effects) else 10

    # Fill remaining slots (up to 4 effects) with random effects
    while len(effects) < 4:
        effect_type = random.choice(["buff", "debuff", "dual"])
        if effect_type == "buff":
            effect = {"name": f"{race_name} Boost", "value": f"+{random.randint(5, 15)} {random.choice(['Attack', 'Defense', 'Speed', 'HP'])}", "type": "normal"}
        elif effect_type == "debuff":
            effect = {"name": f"{race_name} Weakness", "value": f"-{random.randint(5, 10)} {random.choice(['Attack', 'Defense', 'Speed', 'HP'])}", "type": "normal"}
        else:  # dual
            element = random.choice(['Fire', 'Water', 'Ice', 'Electric', 'Earth', 'Nature', 'Metal', 'Air', 'Light', 'Shadow', 'Life', 'Death'])
            effect = {"name": f"{race_name} Power", "value": f"+{random.randint(20, 35)}% {element} Damage", "type": "dual", "weakness": random.choice(['Fire', 'Water', 'Ice', 'Electric', 'Earth', 'Nature', 'Metal', 'Air', 'Light', 'Shadow', 'Life', 'Death']), "strength": element}
        if effect["name"] not in [e["name"] for e in effects]:
            effects.append(effect)
            power_index += 5 if effect["type"] == "normal" else 10

    power_index = min(power_index, 50)  # Cap power index at 50%
    print(f"Generated race effects for {race_name} with color {color} (class: {class_type}, attrs: {attributes}): {effects}, power_index: {power_index}")
    return {"effects": effects, "power_index": power_index}

