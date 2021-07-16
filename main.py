#!/bin/python3

from PIL import Image, ImageDraw
from copy import deepcopy


def make_cells(seed, width, height):
    i, j = 0, 0
    splitted = seed.split(".")
    new_cells = [[0 for x in range(width)] for xx in range(height)]
    for line in splitted:
        for char in line:
            new_cells[j][i] = (char != " ")
            i += 1
        i = 0
        j += 1
    return new_cells


def is_active(cells, x, y):
    try:
        return cells[x][y]
    except IndexError:
        return False


def amount_of_neighbors(cells, posx, posy):
    neighbors = 0
    neighbors += 1 if is_active(cells, posx-1, posy-1) else 0
    neighbors += 1 if is_active(cells, posx, posy-1) else 0
    neighbors += 1 if is_active(cells, posx+1, posy-1) else 0
    neighbors += 1 if is_active(cells, posx-1, posy) else 0
    neighbors += 1 if is_active(cells, posx+1, posy) else 0
    neighbors += 1 if is_active(cells, posx-1, posy+1) else 0
    neighbors += 1 if is_active(cells, posx, posy+1) else 0
    neighbors += 1 if is_active(cells, posx+1, posy+1) else 0
    return neighbors


def calc_new_state():
    for cur_cell_x in range(len(cells)):
        for cur_cell_y in range(len(cells[cur_cell_x])):
            neighbors = amount_of_neighbors(old_cells, cur_cell_x, cur_cell_y)
            if cells[cur_cell_x][cur_cell_y] and (neighbors < 2) or (neighbors > 3):
                cells[cur_cell_x][cur_cell_y] = False
            elif neighbors == 3:
                cells[cur_cell_x][cur_cell_y] = True

    return cells


w, h = 10, 20
tile_size = 25
# Start a new-line with a "." dot.
# Everything else than a " " space is an active cell.
init_state = "     ." + \
             "  #  ." + \
             "  #  ." + \
             "  #  ." + \
             "     ."


cells = make_cells(init_state, w, h)
old_cells = deepcopy(cells)

# Do things.
frames = []
# 10 frames to render.
for frame in range(25):
    # PIL accesses images in Cartesian co-ordinates, so it is Image[columns, rows]
    frames.append(Image.new('RGB', (1000, 1000), "#555"))  # create a new black image
    # frames.append(Image.new('RGB', ((tile_size * w) + 1, ((tile_size * h) + 1)), "#555"))  # create a new black image
    pixels = frames[frame].load()  # create the pixel map

    for cell_x in range(len(cells)):
        for cell_y in range(len(cells[cell_x])):
            draw_cell = [(cell_x * tile_size + 1, cell_y * tile_size + 1), ((cell_x + 1) * tile_size - 1), ((cell_y + 1) * tile_size - 1)]
            # create rectangle image
            square = ImageDraw.Draw(frames[frame])
            print(cell_x, cell_y)
            colour = "#fff" if cells[cell_x][cell_y] else "#000"
            square.rectangle(draw_cell, fill=colour)

    old_cells = deepcopy(cells)
    cells = calc_new_state()

# render the gif
frames[0].save('out.gif', save_all=True, append_images=frames[1:], optimize=False, loop=0, duration=250)
