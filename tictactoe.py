#contreras

def print_board(board):
    print("\n")
    for i in range(0, 9, 3):
        a, b, c = board[i], board[i+1], board[i+2]
        print(f" {a} | {b} | {c} ")
        if i < 6:
            print("---+---+---")
    print("\n")

LINES = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),
    (0, 3, 6), (1, 4, 7), (2, 5, 8),
    (0, 4, 8), (2, 4, 6)
]

def winner(board):
    for a, b, c in LINES:
        if board[a] != ' ' and board[a] == board[b] == board[c]:
            return board[a]
    return None

def moves(board):
    return [i for i, v in enumerate(board) if v == ' ']

def terminal(board):
    return winner(board) is not None or not moves(board)

def utility(board, me='O', opp='X'):
    w = winner(board)
    if w == me:
        return 1
    elif w == opp:
        return -1
    return 0

minimax_nodes = 0

def minimax(board, player, me='O', opp='X'):
    global minimax_nodes
    minimax_nodes += 1
    if terminal(board):
        return utility(board, me, opp), None
    best_val = -2 if player == me else 2
    best_move = None
    for m in moves(board):
        b2 = board[:]
        b2[m] = player
        next_player = opp if player == me else me
        val, _ = minimax(b2, next_player, me, opp)
        if player == me and val > best_val:
            best_val, best_move = val, m
        elif player == opp and val < best_val:
            best_val, best_move = val, m
        if (player == me and best_val == 1) or (player == opp and best_val == -1):
            break
    return best_val, best_move

alphabeta_nodes = 0

def alphabeta(board, player, alpha=-2, beta=2, me='O', opp='X'):
    global alphabeta_nodes
    alphabeta_nodes += 1
    if terminal(board):
        return utility(board, me, opp), None
    if player == me:
        best = (-2, None)
        for m in moves(board):
            b2 = board[:]; b2[m] = player
            val, _ = alphabeta(b2, opp, alpha, beta, me, opp)
            if val > best[0]:
                best = (val, m)
            alpha = max(alpha, val)
            if alpha >= beta:
                break
        return best
    else:
        best = (2, None)
        for m in moves(board):
            b2 = board[:]; b2[m] = player
            val, _ = alphabeta(b2, me, alpha, beta, me, opp)
            if val < best[0]:
                best = (val, m)
            beta = min(beta, val)
            if alpha >= beta:
                break
        return best

def play_game():
    board = [' '] * 9
    human = 'X'
    ai = 'O'
    print("Welcome to Tic-Tac-Toe (You are X, AI is O)")
    print_board(board)
    first = input("Do you want to go first? (y/n): ").strip().lower().startswith('y')
    current = human if first else ai
    while not terminal(board):
        if current == human:
            try:
                pos = int(input("Enter your move (1-9): ")) - 1
            except ValueError:
                print("Please enter a number 1-9.")
                continue
            if pos not in range(9) or pos not in moves(board):
                print("Invalid move. Try again.")
                continue
            board[pos] = human
        else:
            print("AI is thinking...")
            global alphabeta_nodes
            alphabeta_nodes = 0
            _, m = alphabeta(board, player=ai, alpha=-2, beta=2, me=ai, opp=human)
            if m is None:
                m = moves(board)[0]
            board[m] = ai
            print(f"AI chose position {m+1}")
            print(f"(Nodes visited: {alphabeta_nodes})")
        print_board(board)
        current = ai if current == human else human
    w = winner(board)
    if w == human:
        print("🎉 You win!")
    elif w == ai:
        print("🤖 AI wins!")
    else:
        print("😐 It's a draw!")

def compare_search(board, me='O', opp='X'):
    global minimax_nodes, alphabeta_nodes
    minimax_nodes = 0
    val_min, mv_min = minimax(board[:], player=me, me=me, opp=opp)
    mnodes = minimax_nodes
    alphabeta_nodes = 0
    val_ab, mv_ab = alphabeta(board[:], player=me, alpha=-2, beta=2, me=me, opp=opp)
    anodes = alphabeta_nodes
    print_board(board)
    print(f"Minimax  -> value={val_min}, move={(mv_min+1) if mv_min is not None else None}, nodes={mnodes}")
    print(f"AlphaBeta-> value={val_ab}, move={(mv_ab+1) if mv_ab is not None else None}, nodes={anodes}")

if __name__ == "__main__":
    test_board = ['X','O','X','O','X',' ',' ','O',' ']
    compare_search(test_board[:], me='O', opp='X')
    play = input("Start game? (y/n): ").strip().lower().startswith('y')
    if play:
        play_game()

