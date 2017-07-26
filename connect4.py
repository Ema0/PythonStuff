symbols = {1: 'X', 2: 'O'}

def print_board(board):
    """Print the board scheme"""
    tokens = {('0', '0'): ' ', 
              ('1', '0'): symbols[1],
              ('0', '1'): symbols[2]}
    board1, board2 = board.values()
    labels = ('\n ' + '  {} '*7 + ' \n').format(1,2,3,4,5,6,7)
    output = '-'*31 + labels
    for a in range(6):
        tmp = '|'
        for b in range(7):
            index = 7*b + a
            b1 = board1[index]
            b2 = board2[index]
            tmp += '  {} '.format(tokens[b1, b2])
        tmp += ' |\n'
        output = '|{}|\n{}{}'.format(' '*29, tmp, output)
    print output


def check_winner(board):
    """
    Check the player's board to see if it has won
    It uses the algorithm from Fhourstones Benchmark from John Tromp
    https://stackoverflow.com/a/7053051
    """
    b_board = int(board, 2)
    y = b_board & (b_board >> 6)
    if (y & (y >> 2 * 6)):    # check \ diagonal
        return True
    y = b_board & (b_board >> 7)
    if (y & (y >> 2 * 7)):    # check horizontal
        return True
    y = b_board & (b_board >> 8)
    if (y & (y >> 2 * 8)):    # check / diagonal
        return True
    y = b_board & (b_board >> 1)
    if (y & (y >> 2)):        # check vertical
        return True
    return False


def check_draw(boards):
    """Check if the game is in a drawing position (board full & no winner)"""
    board1, board2 = boards.values()
    full_board = format(int(board1, 2) | int(board2, 2), '049b')
    if full_board.count('0') == 7:
        return True
    else:
        return False


def get_move(player):
    """
    Ask the player for their move.
    Get column number (1-7) from raw input
    and returns the int column number (0-6)
    """
    while True:
        input_column = raw_input('Player {}, enter column: '.format(player))
        try: column = int(input_column) - 1
        except ValueError: continue
        if column in range(7):
            return column
        else:
            print 'Non-existent column. Insert a value between 1 and 7.'


def turn(boards, player):
    """
    Player turn, set the new board after asking the move to the player
    Returns the board dictionary
    """
    board1, board2 = boards.values()
    while True:
        column_num = get_move(player)
        start = column_num * 7
        end   = start + 6
        for index, i in enumerate(range(start, end)):
            if board1[i] == board2[i] == '0':
                new_player_board = list(boards[player])
                new_player_board[column_num*7 + index] = '1'
                boards[player] = ''.join(new_player_board)
                return boards
        print 'Column full. Choose another column.'


def play():
    """Handle turns for each player"""
    boards = {1: '0'*49, 2: '0'*49}
    print_board(boards)
    turn_number = 0
    while True:
        turn_number += 1
        player = 1 if turn_number%2 == 1 else 2
        boards = turn(boards, player)
        print_board(boards)
        board  = boards[player]
        winner = check_winner(board)
        if winner:
            print 'Player {} wins!'.format(player)
            return
        draw = check_draw(boards)
        if draw:
            print "It's a draw!"
            return
            


def main():
    """Main. Print banner and starts the game"""
    print '\nWelcome!\n\n' + \
          '    Player 1: {}\n'.format(symbols[1]) + \
          '    Player 2: {}\n'.format(symbols[2]) + \
          '\nEnter the column in which to place the token (1-7)\n'
    try: play()
    except KeyboardInterrupt: return


if __name__=='__main__':
    main()