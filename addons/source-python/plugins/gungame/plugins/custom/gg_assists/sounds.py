# ../gungame/plugins/custom/gg_assists/sounds.py

"""Register sounds for gg_assists."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# GunGame
from gungame.core.sounds.manager import sound_manager


# =============================================================================
# >> SOUND REGISTRATION
# =============================================================================
sound_manager.register_sound(
    sound_name='can_redeem_assists',
    default='buttons/weapon_confirm.wav',
)
