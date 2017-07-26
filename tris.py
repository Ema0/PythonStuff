def print_banner():
    print 'Wrong move number! Insert number between 0-9'
    print 'Moves meanings are:'
    print_grid(range(1,11))   


def get_move(player):
    move = None
    while True:
        input_move = raw_input('Player {}, enter move: '.format(player))
        try: move = int(input_move) - 1
        except ValueError: continue
        if move in range(10):
            return move
        else:
            print_banner()


def print_grid(grid):
    ascii_grid = ' {} | {} | {}  \n----------- \n'*2 + \
                 ' {} | {} | {}  \n'
    print '\n'
    print ascii_grid.format(grid[0], grid[1], grid[2],
                            grid[3], grid[4], grid[5],  
                            grid[6], grid[7], grid[8])


def check_winner(grid, symbol, winnings):
    if ' ' not in grid:
        return 'Draw'
    for winning_conf in winnings:
        if grid[winning_conf[0]] ==  \
           grid[winning_conf[1]] ==  \
           grid[winning_conf[2]] == symbol:
            return symbol
    return False


def turn(grid, player, symbol):
    while True:
        move = get_move(player)
        if grid[move] is ' ':
            grid[move] = symbol
            print_grid(grid)
            return grid
        else:
            print 'Cell already taken. Insert another move.'


def play():
    grid = [' ']*9
    winnings = [(0,1,2), (0,4,8), (0,3,6), (1,4,7), 
                (2,4,6), (2,5,8), (3,4,5), (6,7,8)]
    symbols = {1: 'X', 2: 'O'}
    turn_number = 0
    while True:
        turn_number += 1
        player = 1 if turn_number%2 == 1 else 2
        symbol = symbols[player]
        grid = turn(grid, player, symbol)
        winner = check_winner(grid, symbol, winnings)
        if winner == 'Draw':
            print 'It\'s a draw!'
            return
        elif winner:
            print 'Player {} wins!'.format(player)
            return


def main():
    print_banner()
    play()


if __name__ == '__main__':
    main()