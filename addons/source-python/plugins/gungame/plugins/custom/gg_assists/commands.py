# ../gungame/plugins/custom/gg_assists/commands.py

"""Command registration for gg_assists."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# GunGame
from gungame.core.commands.registration import register_command_callback
from gungame.core.players.dictionary import player_dictionary
from gungame.core.status import GunGameMatchStatus, GunGameStatus
from gungame.core.weapons.groups import melee_weapons, all_grenade_weapons
from gungame.core.weapons.manager import weapon_order_manager


# =============================================================================
# >> FUNCTIONS
# =============================================================================
@register_command_callback('assists', 'Assists:Command')
def _redeem_assist_points_callback(index):
    from .configuration import (
        allow_win, level_increase, start_amount, skip_nade, skip_knife,
    )
    if GunGameStatus.MATCH is not GunGameMatchStatus.ACTIVE:
        return

    player = player_dictionary.from_index(index)
    if player.level_weapon in all_grenade_weapons and not skip_nade.get_bool():
        player.chat_message(
            message='Assists:Denied:Level',
            index=player.index,
            weapon=player.level_weapon,
        )
        return

    if player.level_weapon in melee_weapons and not skip_knife.get_bool():
        player.chat_message(
            message='Assists:Denied:Level',
            index=player.index,
            weapon=player.level_weapon,
        )
        return

    if (
        player.level == weapon_order_manager.max_levels
        and not allow_win.get_bool()
    ):
        player.chat_message(
            message='Assists:Denied:Win',
            index=player.index,
        )
        return

    amount = start_amount.get_int()
    amount += player.level * level_increase.get_int()

    if amount > player.assist_points:
        player.chat_message(
            message='Assists:Denied:Points',
            index=player.index,
            current=player.assist_points,
            required=amount,
        )
        return

    current = player.level
    player.increase_level(1, 'assists')
    if player.level <= current:
        player.chat_message(
            message='Assists:Failed',
            index=player.index,
        )
        return

    player.chat_message(
        message='Assists:Redeemed',
        index=player.index,
        points=amount,
    )
    player.assist_points -= amount
