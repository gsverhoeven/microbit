'''
Conway's Game Of Life for the micro:bit

Press button A or tap the micro:bit to generate a fresh layout.
'''

import microbit

arena1 = [[0, 0, 0, 0, 0],
          [0, 1, 1, 1, 0],
          [0, 0, 0, 1, 0],
          [0, 0, 1, 0, 0],
          [0, 0, 0, 0, 0]]

arena2 = [[0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0]]


def show():
    img = microbit.Image(5, 5)
    for x in range(5):
        for y in range(5):
            img.set_pixel(x, y, arena1[x][y]*9)
    microbit.display.show(img)

def pb(coord): # periodic boundary along one axis
    if coord > 4: 
        return 0; 
    if coord < 0:
        return 4;
    else: 
        return coord;

# do 1 iteration of Conway's Game of Life
def conway_step():
    global arena1, arena2
    cell_state = 0;
    for x in range(5):
        for y in range(5):
            # count number of neighbours
            num_neighbours = (arena1[pb(x - 1)][pb(y - 1)] + # pixel above
                    arena1[pb(x - 1)][y]  +
                    arena1[pb(x - 1)][pb(y + 1)]  +
                    arena1[x][pb(y - 1)]  +
                    arena1[x][pb(y + 1)]  +
                    arena1[pb(x + 1)][pb(y - 1)]  +
                    arena1[pb(x + 1)][y]  +
                    arena1[pb(x + 1)][pb(y + 1)]
                   )
            # check if the centre cell is alive or not
            cell_state = arena1[x][y]
            # apply the rules of life
            if cell_state and not (2 <= num_neighbours <= 3):
                arena2[x][y] = 0  # not enough, or too many neighbours: cell dies
            elif not cell_state and num_neighbours == 3:
                arena2[x][y] = 1  # exactly 3 neighbours around empty cell: cell born
            else:
                arena2[x][y] = cell_state  # stay as-is
    # swap the buffers (arena1 is now the new one to display)
    for x in range(5):
        for y in range(5):
        # count number of neighbours
            arena1[x][y] = arena2[x][y] 


def program_init_state():
    j = 0
    x = 0
    y = 0
    microbit.sleep(100)
    while j < 25:     
        if microbit.button_a.was_pressed():
            arena1[x][y] = not arena1[x][y]
            show()
            microbit.sleep(1)
        if microbit.button_b.was_pressed():
            x = x + 1
            if x == 5:
                x = 0
                y = y  + 1
            j = j + 1
        else:
            microbit.sleep(100)


def reset_arena1():
    global arena1
    arena1 = [[0, 0, 0, 0, 0],
          [0, 1, 1, 1, 0],
          [0, 0, 0, 1, 0],
          [0, 0, 1, 0, 0],
          [0, 0, 0, 0, 0]]


def init_choice():
    microbit.button_b.was_pressed()
    microbit.sleep(100)
    microbit.display.scroll("A or B")
    while True:
        if microbit.button_a.was_pressed():
            choice = "A"
            break
        if microbit.button_b.was_pressed():
            choice = "B"
            break
    microbit.display.scroll(choice)
    if choice == "A":
        show()
        microbit.sleep(100)
        return
    if choice == "B":
        program_init_state()
        return


while True:
    # show basic glider as default
    reset_arena1()
    init_choice()
    # after all pixels are set: cycle through game of life with a button
    # reset with b
    microbit.sleep(1000)
    while not microbit.button_b.is_pressed():
        if microbit.button_a.was_pressed():
            conway_step()
            show()
        else:
            microbit.sleep(100)
