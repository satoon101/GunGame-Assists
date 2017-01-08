# ../gungame/plugins/custom/gg_assists/rules.py

"""Creates the gg_assists rules."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# GunGame
from gungame.core.rules.instance import GunGameRules
from gungame.core.rules.strings import rules_translations

# Plugin
from .info import info


# =============================================================================
# >> RULES
# =============================================================================
assists_rules = GunGameRules(info.name)
assists_rules.title = 'AssistsRules'
for _key, _value in rules_translations.items():
    if _key.startswith('AssistsRules:'):
        assists_rules.register_rule(
            name=_key,
            value=_value,
        )
