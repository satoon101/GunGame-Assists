# ../gungame/plugins/custom/gg_assists/commands.py

"""Command registration for gg_assists."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# GunGame
from gungame.core.commands.registration import register_command_callback
from gungame.core.players.dictionary import player_dictionary
from gungame.core.weapons.groups import melee_weapons, all_grenade_weapons
from gungame.core.weapons.manager import weapon_order_manager


# =============================================================================
# >> FUNCTIONS
# =============================================================================
@register_command_callback('assists', 'Assists:Command')
def _redeem_assist_points_callback(index):
    from .configuration import (
        allow_win, level_increase, notify, play_sound, start_amount, skip_nade,
        skip_knife,
    )

    player = player_dictionary.from_index(index)
    if player.level_weapon in all_grenade_weapons and not skip_nade.get_bool():
        # TODO: send message
        return

    if player.level_weapon in melee_weapons and not skip_knife.get_bool():
        # TODO: send message
        return

    if (
        player.level == weapon_order_manager.max_levels
        and not allow_win.get_bool()
    ):
        # TODO: send message
        return

    amount = start_amount.get_int()
    amount += player.level * level_increase.get_int()

    if amount > player.assist_points:
        # TODO: send message
        return

    current = player.level
    player.increase_level(1, 'assists')
    if player.level <= current:
        # TODO: send message
        return

    player.assist_points -= amount
