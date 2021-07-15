#!/bin/python3

from PIL import Image, ImageDraw
from copy import deepcopy

w, h = 5, 5
init_state = "     " + \
             "  #  " + \
             "  #  " + \
             "  #  " + \
             "     "


def make_cells(init_state):
    i, j = 0, 0
    new_cells = [[0 for x in range(w)] for y in range(h)]
    for char in range(0, len(init_state)):
        new_cells[i][j] = True if init_state[char] == "#" else False

        # Up i, j's based on the w, h's
        i += 1
        if i == w:
            i = 0
            j += 1
        if j == h:
            return new_cells


cells = make_cells(init_state)
old_cells = deepcopy(cells)


def amount_of_neighbors(cells, posx, posy):
    neighbors = 0
    # All left neighbors.
    if posx > 0:
        if cells[posx - 1][posy]:
            neighbors += 1
        if posy > 0 and cells[posx - 1][posy - 1]:
            neighbors += 1
        if posy < (h - 1) and cells[posx - 1][posy + 1]:
            neighbors += 1
    # All right neighbors.
    if posx < (w - 1):
        if cells[posx + 1][posy]:
            neighbors += 1
        if posy > 0 and cells[posx + 1][posy - 1]:
            neighbors += 1
        if posy < (h - 1) and cells[posx + 1][posy + 1]:
            neighbors += 1

    # Top neighbor
    if posy > 0 and cells[posx][posy - 1]:
        neighbors += 1
    # Bottom neighbor
    if posy < (h - 1) and cells[posx][posy + 1]:
        neighbors += 1
    return neighbors


def calc_new_state():
    x, y = 0, 0
    for row in old_cells:
        x = 0
        for cell in row:
            neighbors = amount_of_neighbors(old_cells, x, y)

            if cells[x][y]:
                if (neighbors < 2) or (neighbors > 3):
                    cells[x][y] = False
            else:
                if neighbors == 3:
                    cells[x][y] = True

            x += 1
        y += 1
    return cells


# Do things.
frames = []
# 10 frames to render.
for frame in range(25):
    # PIL accesses images in Cartesian co-ordinates, so it is Image[columns, rows]
    frames.append(Image.new('RGB', (251, 251), "#555"))  # create a new black image
    pixels = frames[frame].load()  # create the pixel map

    x, y = 0, 0
    for row in cells:
        x = 0
        for cell in row:
            draw_cell = [(x * 50 + 1, y * 50 + 1), ((x + 1) * 50 - 1), ((y + 1) * 50 - 1)]
            # create rectangle image
            square = ImageDraw.Draw(frames[frame])
            # print("[" + str(x) + "][" + str(y) + "]: " + str(cells[x][y]))
            if old_cells[x][y] != cells[x][y]:
                if cells[x][y]:
                    colour = "#6f6"
                else:
                    colour = "#f66"
            else:
                colour = "#fff" if cells[x][y] else "#000"

            square.rectangle(draw_cell, fill=colour)

            x += 1
        y += 1
    old_cells = deepcopy(cells)
    cells = calc_new_state()

# render the gif
frames[0].save('out.gif', save_all=True, append_images=frames[1:], optimize=False, loop=0, duration=250)
