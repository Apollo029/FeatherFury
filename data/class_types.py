# data/class_types.py
from typing import List, Dict
from data.classes import CLASS_STATS
import random
from data.attributes import PRIMARY_ATTRIBUTES

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
            "losses_to_bots": 0,
            "monthly_trophies": 0,
            "quarterly_trophies": 0
        }
        self.combo_used = False
        self.damage_dealt_in_battle = 0

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

async def generate_race_effects(race_name: str, color: str, class_type: str = None, attributes: List[str] = None, is_bot: bool = False) -> Dict:
    """Generate race effects based on attributes with balanced dynamic generation."""
    effects = []
    power_index = 0

    # Define a smaller set of elements and stat types to reduce random calls
    stat_types = ['Attack', 'Defense', 'Speed', 'HP']
    elements = ['Fire', 'Water', 'Ice', 'Electric', 'Earth', 'Nature', 'Metal', 'Air', 'Light', 'Shadow', 'Life', 'Death']
    # Precompute possible weaknesses for each element
    element_weaknesses = {element: [e for e in elements if e != element] for element in elements}

    # Precompute choices to reduce random calls
    effect_types = ["buff", "debuff", "dual"]
    if is_bot:
        effect_types = ["buff", "buff", "debuff"]  # More likely to get buffs

    # Fill up to 4 effects with dynamic effects
    while len(effects) < 4:
        effect_type = random.choice(effect_types)
        if effect_type == "buff":
            stat = random.choice(stat_types)
            value = random.randint(5, 10) if is_bot else random.randint(5, 15)
            effect = {"name": f"{race_name} Boost", "value": f"+{value} {stat}", "type": "normal"}
        elif effect_type == "debuff":
            stat = random.choice(stat_types)
            value = random.randint(3, 5) if is_bot else random.randint(5, 10)
            effect = {"name": f"{race_name} Weakness", "value": f"-{value} {stat}", "type": "normal"}
        else:  # dual
            element = random.choice(elements)
            value = random.randint(20, 35)
            weakness = random.choice(element_weaknesses[element])
            effect = {"name": f"{race_name} Power", "value": f"+{value}% {element} Damage", "type": "dual", "weakness": weakness, "strength": element}
        if effect["name"] not in [e["name"] for e in effects]:
            effects.append(effect)
            power_index += 5 if effect["type"] == "normal" else 10
        # Add a small delay to prevent blocking
        await asyncio.sleep(0.1)

    power_index = min(power_index, 50)  # Cap power index at 50%
    print(f"Generated race effects for {race_name} with color {color} (class: {class_type}, attrs: {attributes}, is_bot: {is_bot}): {effects}, power_index: {power_index}")
    return {"effects": effects, "power_index": power_index}
