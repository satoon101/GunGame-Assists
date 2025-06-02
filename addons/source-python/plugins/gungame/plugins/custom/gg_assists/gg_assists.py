# ../gungame/plugins/custom/gg_assists/gg_assists.py

"""Plugin that allows players to gain levels from assisting in kills."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Python
from collections import defaultdict

# Source.Python
from events import Event
from players.entity import Player

# GunGame
from gungame.core.commands.registration import command_dictionary
from gungame.core.players.attributes import player_attributes
from gungame.core.players.dictionary import player_dictionary
from gungame.core.status import GunGameMatchStatus, GunGameStatus

# Plugin
from .configuration import (
    alive_only,
    level_increase,
    notify,
    percent,
    play_sound,
    start_amount,
)

# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
player_assist_points = defaultdict(lambda: defaultdict(int))


# =============================================================================
# >> LOAD & UNLOAD
# =============================================================================
def load():
    """Add the player assist attribute."""
    player_attributes.register_attribute("assist_points", 0)


def unload():
    """Remove the player assist attribute."""
    player_attributes.unregister_attribute("assist_points")


# =============================================================================
# >> GAME EVENTS
# =============================================================================
@Event("player_hurt")
def _add_damage(game_event):
    if GunGameStatus.MATCH is not GunGameMatchStatus.ACTIVE:
        return

    attacker = game_event["attacker"]
    userid = game_event["userid"]
    if attacker in (userid, 0):
        return

    killer = player_dictionary[attacker]
    victim = player_dictionary[userid]
    if killer.team_index == victim.team_index:
        return

    player_assist_points[attacker][userid] += game_event["dmg_health"]


# ruff: noqa: C901
@Event("player_death")
def _add_assist_points(game_event):
    if GunGameStatus.MATCH is not GunGameMatchStatus.ACTIVE:
        return

    attacker = game_event["attacker"]
    victim = game_event["userid"]

    # Reset the victim's assist points on death
    if victim in player_assist_points and bool(alive_only):
        del player_assist_points[victim]

    # Do not add assist points for kill
    if (
        attacker in player_assist_points and
        victim in player_assist_points[attacker]
    ):
        del player_assist_points[attacker][victim]

    current_percent = int(percent) / 100 or 100
    for userid in list(player_assist_points):
        if victim not in player_assist_points[userid]:
            continue

        try:
            Player.from_userid(userid)
        except ValueError:
            continue

        # Add assist points for the current player
        points = player_assist_points[userid].pop(victim)
        player = player_dictionary[userid]
        player.assist_points += points * current_percent

        # Notify the player if they can redeem points
        required = int(start_amount)
        required += player.level * int(level_increase)
        if player.assist_points >= required:
            if notify:
                player.chat_message(
                    "Assists:Earned",
                    command=command_dictionary["assists"].commands[0],
                )
            if play_sound:
                player.play_gg_sound("can_redeem_assists")

        if not player_assist_points[userid]:
            del player_assist_points[userid]


@Event("player_spawn")
def _clear_player_assists(game_event):
    if GunGameStatus.MATCH is not GunGameMatchStatus.ACTIVE:
        return

    userid = game_event["userid"]
    if userid in player_assist_points:
        del player_assist_points[userid]
