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
from gungame.core.players.attributes import player_attributes
from gungame.core.players.dictionary import player_dictionary
from gungame.core.status import GunGameMatchStatus, GunGameStatus

# Plugin
from .configuration import alive_only, level_increase, percent, start_amount


# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
player_assist_points = defaultdict(lambda: defaultdict(int))


# =============================================================================
# >> LOAD & UNLOAD
# =============================================================================
def load():
    """Add the player assist attribute."""
    player_attributes.register_attribute('assist_points', 0)


def unload():
    """Remove the player assist attribute."""
    player_attributes.unregister_attribute('assist_points')


# =============================================================================
# >> GAME EVENTS
# =============================================================================
@Event('player_hurt')
def _add_damage(game_event):
    if GunGameStatus.MATCH is not GunGameMatchStatus.ACTIVE:
        return

    attacker = game_event['attacker']
    userid = game_event['userid']
    if attacker in (userid, 0):
        return

    killer = player_dictionary[attacker]
    victim = player_dictionary[userid]
    if killer.team_index == victim.team_index:
        return

    player_assist_points[attacker][userid] += game_event['dmg_health']


@Event('player_death')
def _add_assist_points(game_event):
    if GunGameStatus.MATCH is not GunGameMatchStatus.ACTIVE:
        return

    attacker = game_event['attacker']
    victim = game_event['userid']
    if victim in player_assist_points and not alive_only.get_bool():
        del player_assist_points[victim]

    if (
        attacker in player_assist_points and
        victim in player_assist_points[attacker]
    ):
        del player_assist_points[attacker][victim]

    for userid in list(player_assist_points):
        if victim not in player_assist_points[userid]:
            continue

        try:
            Player.from_userid(userid)
        except ValueError:
            continue

        points = player_assist_points[userid].pop(victim)
        current_percent = percent.get_int() / 100 or 100
        player = player_dictionary[userid]
        player.assist_points += points * current_percent

        required = start_amount.get_int()
        required += player.level * level_increase.get_int()
        if player.assist_points >= required:
            player.chat_message(
                'Assists:Earned',
            )
        if not player_assist_points[userid]:
            del player_assist_points[userid]


@Event('player_spawn')
def _clear_player_assists(game_event):
    if GunGameStatus.MATCH is not GunGameMatchStatus.ACTIVE:
        return

    userid = game_event['userid']
    if userid in player_assist_points:
        del player_assist_points[userid]
