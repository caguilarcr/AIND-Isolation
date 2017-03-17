"""
    This file contains all the heuristics implemented for this project.
"""

def weighted_improved_score(game, player):
    """
    Same as the improved_score heuristic but prioritizing the amount of moves
    the player has over the opponent's remaining moves.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : hashable
        One of the objects registered by the game object as a valid player.
        (i.e., `player` should be either game.__player_1__ or
        game.__player_2__).

    Returns
    ----------
    float
        The heuristic value of the current game state
    """
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    own_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))
    return float(10 * own_moves -  5 * opp_moves)

'''
    Moves used for the future_moves_weight heuristic, they are declared here
    to improve the heuristic performance.
'''
# 3th level
row_minus_one_column_cero = [(-2, -2), (-2, 2)]
row_plus_one_column_cero = [(2, -2), (2, 2)]
row_cero_column_minus_one = [(-2, -2), (-2, 2)]
row_cero_column_plus_one = [(-2, 2), (2, 2)]
# 2nd level
row_cero_column_minus_two = {
    (-1, 0): row_minus_one_column_cero,
    (1, 0) : row_plus_one_column_cero
}
row_minus_one_column_plus_one = {
    (0, -1): row_cero_column_minus_one,
    (1, 0): row_plus_one_column_cero,
}
row_minus_two_column_cero = {
    (0, -1): row_cero_column_minus_one,
    (0, 1): row_cero_column_plus_one
}
row_plus_one_column_minus_one = {
    (-1, 0): row_minus_one_column_cero,
    (0, 1): row_cero_column_plus_one,
}
row_minus_one_column_minus_one = {
    (0, 1): row_cero_column_plus_one,
    (1, 0): row_plus_one_column_cero,
}
row_plus_two_column_cero = {
    (0, -1): row_cero_column_minus_one,
    (0, 1): row_cero_column_plus_one
}
row_plus_one_column_plus_one = {
    (-1, 0): row_minus_one_column_cero,
    (0, -1): row_cero_column_minus_one
}
row_cero_column_plus_two = {
    (-1, 0): row_minus_one_column_cero,
    (1, 0): row_plus_one_column_cero
}
# 1st level
directions = {
    (-2, -1): {
        (0, -2): row_cero_column_minus_two,
        (-1, 1): row_minus_one_column_plus_one
    },
    (-1, -2): {
        (-2, 0): row_minus_two_column_cero,
        (1, -1): row_plus_one_column_minus_one
    },
    (1, -2): {
        (-1, -1): row_minus_one_column_minus_one,
        (2, 0): row_plus_two_column_cero
    },
    (2, -1): {
        (0, -2) : row_cero_column_minus_two,
        (1, 1): row_plus_one_column_plus_one
    },
    (2, 1): {
        (0, 2) : row_cero_column_plus_two,
        (1, -1): row_minus_one_column_minus_one
    },
    (1, 2): {
        (-1, 1): row_minus_one_column_plus_one,
        (2, 0): row_plus_two_column_cero
    },
    (-1, 2): {
        (-2, 0): row_minus_two_column_cero,
        (1, 1): row_plus_one_column_plus_one
    }
}

def future_moves_weight(game, player):
    """
    Analysis how many moves the player can do at on a simple 5 by 5 grid. It
    assigns weights to the closer moves in order evaluate how much can the
    player move from a certain position. If on a centered enough positions
    it uses the following grid (p is the player's position)

    | 4 | 1 | 2 | 1 | 4 |
    | 1 | 2 | 3 | 2 | 1 |
    | 2 | 3 | p | 3 | 2 |
    | 1 | 2 | 3 | 2 | 1 |
    | 4 | 1 | 2 | 1 | 4 |

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : hashable
        One of the objects registered by the game object as a valid player.
        (i.e., `player` should be either game.__player_1__ or
        game.__player_2__).

    Returns
    ----------
    float
        The heuristic value of the current game state
    """
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    score = 0
    row, col = game.get_player_location(player)
    width = game.width
    height = game.height

    for direction_one in directions:
        row_one, col_one = direction_one
        if game.move_is_legal((row + row_one, col + col_one)):
            score = score + 1
            for direction_two in directions[direction_one]:
                row_two, col_two = direction_two
                if game.move_is_legal((row + row_two, col + col_two)):
                    score = score + 4
                    for direction_three in directions[direction_one][direction_two]:
                        row_three, col_three = direction_three
                        if game.move_is_legal((row + row_three, col + col_three)):
                            score = score + 8
                            for direction_four in directions[direction_one][direction_two][direction_three]:
                                row_four, col_four = direction_four
                                if game.move_is_legal((row + row_four, col + col_four)):
                                    score = score + 16

    return float(score)


def mixed_heuristic(game, player):
    """
    If the board is more than half empty then use difference_player_biased,
    else use future_moves_weight

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : hashable
        One of the objects registered by the game object as a valid player.
        (i.e., `player` should be either game.__player_1__ or
        game.__player_2__).

    Returns
    ----------
    float
        The heuristic value of the current game state
    """
    if game.width * game.height / 2 > len(game.get_blank_spaces()):
        return future_moves_weight(game, player)
    else:
        return difference_player_biased(game, player)
