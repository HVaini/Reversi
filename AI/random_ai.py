def random_ai (board, player):
    empty_count = sum(row.count(empty_slot) for row in board)
    moves = valid_moves(board, player)
    if not moves:
        return None

    if empty_count <= 7:
        print("vaihdettu minimax-ratkaisuun")
        val, best = solve_exact(copy.deepcopy(board), player)
        return best

    return random.choice(moves)