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
    "alive_only",
    "allow_win",
    "level_increase",
    "notify",
    "percent",
    "play_sound",
    "skip_knife",
    "skip_nade",
    "start_amount",
    "use_increase",
)


# =============================================================================
# >> CONFIGURATION
# =============================================================================
with (
    GunGameConfigManager(info.name) as _config,
    _config.cvar("percent", 50) as percent,
    _config.cvar("start_amount", 100) as start_amount,
    _config.cvar("level_increase", 20) as level_increase,
    _config.cvar("use_increase", 100) as use_increase,
    _config.cvar("alive_only") as alive_only,
    _config.cvar("skip_nade") as skip_nade,
    _config.cvar("skip_knife") as skip_knife,
    _config.cvar("allow_win") as allow_win,
    _config.cvar("notify") as notify,
    _config.cvar("play_sound") as play_sound,
):
    percent.add_text()
    start_amount.add_text()
    level_increase.add_text()
    use_increase.add_text()
    alive_only.add_text()
    skip_nade.add_text()
    skip_knife.add_text()
    allow_win.add_text()
    notify.add_text()
    play_sound.add_text()
