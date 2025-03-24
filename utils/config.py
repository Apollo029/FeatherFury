# utils/config.py
import json
import os
from data.constants import DEFAULT_MIN_BATTLE_TOKENS, DEFAULT_MAX_BATTLE_TOKENS

CONFIG_FILE = "server_configs.json"

def load_configs():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    return {}

def save_configs(configs):
    with open(CONFIG_FILE, "w") as f:
        json.dump(configs, f, indent=4)

def get_server_config(guild_id):
    configs = load_configs()
    return configs.get(str(guild_id), {
        "min_battle_tokens": DEFAULT_MIN_BATTLE_TOKENS,
        "max_battle_tokens": DEFAULT_MAX_BATTLE_TOKENS
    })

def update_server_config(guild_id, config):
    configs = load_configs()
    configs[str(guild_id)] = config
    save_configs(configs)
