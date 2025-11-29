import copy, time
from AI.minimax_midgame import minimax_midgame

def iterative_deepening_midgame(board, player, evaluate, 
                                time_limit=2.0, max_depth=60):
    
    start = time.time()
    best_move = None
    best_val = None
    reached_depth = 0

    for depth in range(1, max_depth):

        # Aikaraja
        if time.time() - start >= time_limit:
            break

        hash_moves = {}

        val, move = minimax_midgame(copy.deepcopy(board), player, depth, evaluate, hash_moves= hash_moves)

        

        if move is not None:
            best_move = move
            best_val = val
            reached_depth = depth

        if time.time() - start >= time_limit:
            break

    if best_move is None:
        return (0, None, reached_depth)

    
    print(f"[Mid] saavutettu syvyys {reached_depth}, paras siirto  {best_move}, arvio {best_val}")

    return (best_val, best_move, reached_depth)
