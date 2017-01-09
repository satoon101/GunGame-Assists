# ../gungame/plugins/custom/gg_assists/configuration.py

"""Creates the gg_assists configuration."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# GunGame
from gungame.core.config.manager import GunGameConfigManager

# Plugin
from .info import info


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'alive_only',
    'allow_win',
    'level_increase',
    'percent',
    'skip_knife',
    'skip_nade',
    'start_amount',
)


# =============================================================================
# >> CONFIGURATION
# =============================================================================
with GunGameConfigManager(info.name) as _config:

    with _config.cvar('percent', 50) as percent:
        percent.add_text()

    with _config.cvar('start_amount', 100) as start_amount:
        start_amount.add_text()

    with _config.cvar('level_increase', 20) as level_increase:
        level_increase.add_text()

    with _config.cvar('alive_only') as alive_only:
        alive_only.add_text()

    with _config.cvar('skip_nade') as skip_nade:
        skip_nade.add_text()

    with _config.cvar('skip_knife') as skip_knife:
        skip_knife.add_text()

    with _config.cvar('allow_win') as allow_win:
        allow_win.add_text()
