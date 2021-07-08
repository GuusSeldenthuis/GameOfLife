#!/bin/python3

from PIL import Image, ImageDraw
import random

init_state = "     " + \
             "  #  " + \
             " ### " + \
             "  #  " + \
             "    #"


def make_cells(init_state):
    w, h = 5, 5
    i, j = 0, 0
    new_cells = [[0 for x in range(w)] for y in range(h)]
    for char in range(0, len(init_state)):
        new_cells[i][j] = True if init_state[char] == "#" else False

        # Up i,j's based on the x,y's
        i += 1
        if i == w:
            i = 0
            j += 1
        if j == h:
            return new_cells


cells = make_cells(init_state)
for row in cells:
    print(' '.join([str(elem) for elem in row]))

# DRAW PIXELS
frames = []
# 10 frames to render.
for frame in range(1):
    # PIL accesses images in Cartesian co-ordinates, so it is Image[columns, rows]
    frames.append(Image.new('RGB', (250, 250), "#fff"))  # create a new black image
    pixels = frames[frame].load()  # create the pixel map

    x, y = 0, 0
    for row in cells:
        x = 0
        for cell in row:
            draw_cell = [(x * 50, y * 50), ((x + 1) * 50), ((y + 1) * 50)]
            # create rectangle image
            img1 = ImageDraw.Draw(frames[frame])
            print("[" + str(x) + "][" + str(y) + "]: " + str(cells[x][y]))
            colour = "#fff" if cells[x][y] else "#000"
            img1.rectangle(draw_cell, fill=colour)
            x += 1
        y += 1

# render the gif
frames[0].save('out.gif', save_all=True, append_images=frames[1:], optimize=True, loop=0)
