# ../gungame/plugins/custom/gg_assists/commands.py

"""Command registration for gg_assists."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Python
from collections import defaultdict

# Source.Python
from listeners import OnLevelInit

# GunGame
from gungame.core.commands.registration import register_command_callback
from gungame.core.players.dictionary import player_dictionary
from gungame.core.status import GunGameMatchStatus, GunGameStatus
from gungame.core.weapons.groups import all_grenade_weapons, melee_weapons
from gungame.core.weapons.manager import weapon_order_manager

# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
_redeem_usage = defaultdict(int)


# =============================================================================
# >> FUNCTIONS
# =============================================================================
@register_command_callback("assists", "Assists:Command")
def _redeem_assist_points_callback(index):
    from .configuration import (
        allow_win,
        level_increase,
        skip_knife,
        skip_nade,
        start_amount,
        use_increase,
    )
    if GunGameStatus.MATCH is not GunGameMatchStatus.ACTIVE:
        return

    player = player_dictionary.from_index(index)
    if player.level_weapon in all_grenade_weapons and not bool(skip_nade):
        player.chat_message(
            message="Assists:Denied:Level",
            index=player.index,
            weapon=player.level_weapon,
        )
        return

    if player.level_weapon in melee_weapons and not bool(skip_knife):
        player.chat_message(
            message="Assists:Denied:Level",
            index=player.index,
            weapon=player.level_weapon,
        )
        return

    if (
        player.level == weapon_order_manager.max_levels
        and not bool(allow_win)
    ):
        player.chat_message(
            message="Assists:Denied:Win",
            index=player.index,
        )
        return

    amount = int(start_amount)
    amount += player.level * int(level_increase)
    amount += _redeem_usage[player.userid] * int(use_increase)

    if amount > player.assist_points:
        player.chat_message(
            message="Assists:Denied:Points",
            index=player.index,
            current=player.assist_points,
            required=amount,
        )
        return

    current = player.level
    player.increase_level(1, "assists")
    if player.level <= current:
        player.chat_message(
            message="Assists:Failed",
            index=player.index,
        )
        return

    _redeem_usage[player.userid] += 1
    player.chat_message(
        message="Assists:Redeemed",
        index=player.index,
        points=amount,
    )
    player.assist_points -= amount


@OnLevelInit
def _reset_redeem_usage(map_name):
    """Reset the dictionary."""
    _redeem_usage.clear()
