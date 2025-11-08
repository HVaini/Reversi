from reversi.board import new_board, print_board, play_move, valid_moves, get_opponent, black_piece, white_piece, end_game, count_points


def main():
    board = new_board()
    current_player = black_piece

    while True:
        print_board(board)
        black_score, white_score = count_points(board)
        print(f"\nPisteet  X: {black_score}, O: {white_score}")
        print(f"Vuoro: {current_player}\n")

        # Tarkistetaan pelin loppuminen
        if end_game(board):
            print("\nPeli päättyi")
            if black_score > white_score:
                print(f"Voittaja: X ({black_score} - {white_score})")
            elif white_score > black_score:
                print(f"Voittaja: O ({white_score} - {black_score})")
            else:
                print("Tasapeli")
            break

        valid = valid_moves(board, current_player)
        if not valid:
            print(f"Ei laillisia siirtoja pelaajalle {current_player}.")
            current_player = get_opponent(current_player)

            # Jos 2 kertaa ei siirtoja niin peli päättyy, kumpikaan ei voi siirtää. en tiedä voiko tätä tapahtua kuin ainoastaan silloin kun toisella on kaikki nappulat
            # jos toisella on kaikki nappulat niin sille on oma tarkistus end_game funktiossa mutta pidetään tämäkin toistaiseksi mukana.
            if not valid_moves(board, current_player):
                print("\nKumpikaan ei voi siirtää. Peli päättyi")
                b_score, w_score = count_points(board)
                print(f"Lopulliset pisteet  X: {b_score}, O: {w_score}")
                if b_score > w_score:
                    print("Voittaja: X")
                elif w_score > b_score:
                    print("Voittaja: O")
                else:
                    print("Tasapeli")
                break
            continue

        print(f"Lailliset siirrot: {valid}")
        move_input = input("Anna siirto muodossa 'rivi sarake': ")
        try:
            r, c = map(int, move_input.split())
            if (r, c) in valid:
                play_move(board, (r, c), current_player)
                current_player = get_opponent(current_player)
            else:
                print("Virheellinen siirto, yritä uudelleen.")
        except Exception:
            print("Anna siirto muodossa kaksi numeroa, esim. 2 3.")


if __name__ == "__main__":
    main()
