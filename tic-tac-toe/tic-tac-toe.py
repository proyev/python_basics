def print_field(field):  # prints current field gird
    print('---------')
    print('|', field[0], field[1], field[2], '|')
    print('|', field[3], field[4], field[5], '|')
    print('|', field[6], field[7], field[8], '|')
    print('---------')

def status(field):  # checks the status of the game depending on the field occupancy
    num_O = field.count('O')
    num_X = field.count('X')

    top_row = field[:3]
    middle_row = field[3:6]
    bottom_row = field[6:]

    left_column = field[::3]
    middle_column = field[1::3]
    right_column = field[2::3]

    left_diag = field[0] + field[4] + field[8]  # starts in the top left corner
    right_diag = field[2] + field[4] + field[6]

    # saves all possible combinations from the field to check for status
    combos = [top_row, middle_row, bottom_row, left_column, middle_column, right_column, left_diag, right_diag]

    if abs(num_O - num_X) > 1:
        message = 'Impossible'
        return message
    elif 'XXX' in combos:
        message = 'X wins'
        return message
    elif 'OOO' in combos:
        message = 'O wins'
        return message
    elif '_' not in field:
        message = 'Draw'
        return message
    else:
        message = 'Game not finished'
        return message

def check_validity(turn, coordinates, field_grid):  # checks whether current input is valid
    if coordinates[0].isdigit() and coordinates[1].isdigit():
        # to represent grid coordinates clearer
        x = int(coordinates[0])
        y = int(coordinates[1])
        if 1 <= x <= 3 and 1 <= y <= 3:
            if field_grid[x - 1][y - 1] != '_':  # due to the nature of numbering in a list
                print('This cell is occupied! Choose another one!')
                coordinates = input('Enter the coordinates: ').split()
                check_validity(turn, coordinates, field_grid)
                field = ''.join(field_grid)
                return field
            else:
                update = [position for position in field_grid[x - 1]] # updates the grid if the turn is valid
                update[y - 1] = turn
                field_grid[x - 1] = ''.join(update)
                field = ''.join(field_grid)
                return field
        else:
            print('Coordinates should be from 1 to 3!')
            coordinates = input('Enter the coordinates: ').split()
            check_validity(turn, coordinates, field_grid)
            field = ''.join(field_grid)
            return field
    else:
        print('You should enter numbers!')
        coordinates = input('Enter the coordinates: ').split()
        check_validity(turn, coordinates, field_grid)
        field = ''.join(field_grid)
        return field

# prints initial field grid
field = ('_________')
field_grid = [field[:3], field[3:6], field[6:]]
print_field(field)

# start of the game
turn = 'X'
print('Current turn', turn)
coordinates = input('Enter the coordinates: ').split()
field = check_validity(turn, coordinates, field_grid)
field_grid = [field[:3], field[3:6], field[6:]]
print_field(field)

# game loop itself
while status(field) == 'Game not finished':
    print('Entered the loop')
    if turn == 'X':
        turn = 'O'
        print('Current turn', turn)
        coordinates = input('Enter the coordinates: ').split()
        field = check_validity(turn, coordinates, field_grid)
        print_field(field)
        print(status(field))
        field_grid = [field[:3], field[3:6], field[6:]]
    else:
        turn = 'X'
        print('Current turn', turn)
        coordinates = input('Enter the coordinates: ').split()
        field = check_validity(turn, coordinates, field_grid)
        print_field(field)
        print(status(field))
        field_grid = [field[:3], field[3:6], field[6:]]