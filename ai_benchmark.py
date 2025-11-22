import copy


from reversi.board import (
    new_board,
    print_board,
    valid_moves,
    play_move,
    get_opponent,
    black_piece,
    white_piece,
    end_game,
    count_points,
    empty_slot,
)

from AI.ai_move import ai_move, evaluate_normal, evaluate_longshot
from AI.minimax_midgame import minimax_midgame
from AI.evaluate import evaluate
from AI.minimax_endscore import minimax_endscore



def play_single_game(black_ai, white_ai):

    board = new_board()
    current = black_piece

    while not end_game(board):
        moves = valid_moves(board, current)
        if moves:
            if current == black_piece:
                move = black_ai(copy.deepcopy(board), current)
            else:
                move = white_ai(copy.deepcopy(board), current)


            if move not in moves:
                move = moves[0]

            play_move(board, move, current)

        current = get_opponent(current)

    b, w = count_points(board)
    
    print_board(board)
    print(f"Loppupisteet: B={b}, W={w}")

    if b > w:
        winner = 'B'
    elif w > b:
        winner = 'W'
    else:
        winner = 'D'

    return b, w, winner


def run_matchup(ai1, ai2, games = 20, swap_colors = True):
    

    stats = {
        "games": 0,
        "ai1_wins": 0,
        "ai2_wins": 0,
        "draws": 0,
        "total_margin_ai1": 0,
    }

    for i in range(games):
        if swap_colors and (i % 2 == 1):

            # ai1 pelaa valkoisena, ai2 mustana
            b_ai = ai2
            w_ai = ai1
            ai1_is_black = False
        else:

            # ai1 pelaa mustana, ai2 valkoisena
            b_ai = ai1
            w_ai = ai2
            ai1_is_black = True

        
        print(f"\nPeli {i+1}/{games} (ai1_is_black={ai1_is_black})")

        b, w, winner = play_single_game(b_ai, w_ai)

        # marginaali mustan näkökulmasta
        margin_bw = b - w

        # muutetaan marginaali ai1:n näkökulmasta
        margin_ai1 = margin_bw if ai1_is_black else -margin_bw

        stats["games"] += 1
        stats["total_margin_ai1"] += margin_ai1

        if margin_ai1 > 0:
            stats["ai1_wins"] += 1
        elif margin_ai1 < 0:
            stats["ai2_wins"] += 1
        else:
            stats["draws"] += 1

    return stats


# joitain valmiita matchuppeja alla

def ai_midgame_with_weight(weight, depth):
    

    def eval_with_weight(board, player):
        return evaluate(board, player, weight=weight)

    def ai_weighted(board, player):

        val, move = minimax_midgame(copy.deepcopy(board), player, depth=depth, evaluate=eval_with_weight)
        return move

    return ai_weighted


def ai_mobility_only(depth = 3):


    def eval_mobility_only(board, player):

        # mobility_score + positional_score * weight
        return evaluate(board, player, weight=0)

    def ai_mobility(board, player):
        val, move = minimax_midgame(copy.deepcopy(board), player, depth=depth, evaluate=eval_mobility_only)
        return move

    return ai_mobility


def ai_full_midgame_with_depth(depth: int = 5):

	
    def ai_depth(board, player):
        val, move = minimax_midgame(copy.deepcopy(board), player, depth=depth, evaluate=evaluate_normal)
        return move

    return ai_depth


def ai_full_normal(board, player):
    return ai_move(board, player)

def ai_normal_with_heuristic(weight: int, mid_depth = 5, end_threshold = 10):

    # poistettu longshot-moodi jotta tulokset eivät vääristy

    def eval_weighted(board, player):
        return evaluate(board, player, weight=weight)

    def ai_normal(board, player):
        empty_count = sum(row.count(empty_slot) for row in board)
        moves = valid_moves(board, player)
        if not moves:
            return None

        # ENDGAME → identtinen molemmille AI-versioille
        if empty_count <= end_threshold:
            val, move = minimax_endscore(copy.deepcopy(board), player)
            return move

        # MIDGAME
        val, move = minimax_midgame(
            copy.deepcopy(board),
            player,
            depth=mid_depth,
            evaluate=eval_weighted
        )
        return move

    return ai_normal



if __name__ == "__main__":


    # tällä voi ajaa eri painotuksilla olevia heuristiikkoja vastakkain
    ai_weight_0 = ai_normal_with_heuristic(weight=0, mid_depth=5)  
    ai_weight_1 = ai_normal_with_heuristic(weight=1, mid_depth=5) 
    ai_weight_5 = ai_normal_with_heuristic(weight=5, mid_depth=5)  
    ai_weight_10 = ai_normal_with_heuristic(weight=10, mid_depth=5) 

    # Lista matchupeista
    matchups = [
        ("w=0 (mobility only)",  ai_weight_0,
         "w=5 (default)",        ai_weight_5),

        ("w=1 (mobility-heavy)", ai_weight_1,
         "w=5 (default)",        ai_weight_5),

        ("w=5 (default)",        ai_weight_5,
         "w=10 (matrix-heavy)",  ai_weight_10),

        ("w=0 (mobility only)",  ai_weight_0,
         "w=10 (matrix-heavy)",  ai_weight_10),
    ]

    for name1, ai1, name2, ai2 in matchups:
        print(f"\n {name1}  VS  {name2} ")
        stats = run_matchup(
            ai1,
            ai2,
            games=2,
            swap_colors=True,
        )

        print(f"Pelit: {stats['games']}")
        print(f"{name1} voitot (AI1): {stats['ai1_wins']}")
        print(f"{name2} voitot (AI2): {stats['ai2_wins']}")
        print(f"Tasapelit: {stats['draws']}")
        avg = stats['total_margin_ai1'] / stats['games']
        print(f"Keskimääräinen pistemarginaali AI1:n näkökulmasta: {avg:.2f}")
