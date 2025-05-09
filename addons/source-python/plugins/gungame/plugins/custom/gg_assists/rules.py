# ../gungame/plugins/custom/gg_assists/rules.py

"""Creates the gg_assists rules."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# GunGame
from gungame.core.rules.instance import GunGameRules

# Plugin
from .info import info

# =============================================================================
# >> RULES
# =============================================================================
assists_rules = GunGameRules(info.name)
assists_rules.register_all_rules()
