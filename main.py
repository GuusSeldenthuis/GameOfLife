#!/bin/python3

from PIL import Image, ImageDraw
from copy import deepcopy
import csv

""""
SETTINGS, GLHF.
"""
tile_size = 25  # How big in px are the tiles. (25x25 for example)
# max frames -1 for rendering untill no change. (10000 when -1 to avoid endless loop.)
max_frames = 10
background_color = "#000"  # Tile-frame/background color.
inactive_color = "#060"  # Inactive tile color.
active_color = "#fff"  # Inactive tile color.
# Your comma seperated values file. (Used as source for initial state)
csv_source = "./example.csv"
out_location = "./output.gif"  # Location of the outputted .gif file.
frame_delay = 250  # Amount of ms between frames.
loop_gif = 0  # Set to False to no-loop gif.
""""
END OF SETTINGS.
"""


# 'Safe' way to check for active neighbors despite being outside of the matrix.
def is_active(cells, x, y):
    try:
        return cells[x][y]
    except IndexError:
        return False


# Count all active neighbors.
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


# Da rulez.
def calc_new_state():
    for cur_cell_x in range(len(cells)):
        for cur_cell_y in range(len(cells[cur_cell_x])):
            neighbors = amount_of_neighbors(old_cells, cur_cell_x, cur_cell_y)
            if cells[cur_cell_x][cur_cell_y] and (neighbors < 2) or (neighbors > 3):
                cells[cur_cell_x][cur_cell_y] = False
            elif neighbors == 3:
                cells[cur_cell_x][cur_cell_y] = True

    return cells


# Do loading n' stuff.
cells = list(csv.reader(open(csv_source)))
h, w = len(cells), len(cells[0])
print("Height: %i" % h)
print("Width: %i" % w)
old_cells = deepcopy(cells)

frames = []
for_frames = 10000 if max_frames == -1 else max_frames
for frame in range(for_frames):
    # PIL accesses images in Cartesian co-ordinates, so it is Image[columns, rows]
    frames.append(Image.new('RGB', ((tile_size * h) + 1,
                  ((tile_size * w) + 1)), background_color))
    pixels = frames[frame].load()  # create the pixel map

    for cell_x in range(len(cells)):
        for cell_y in range(len(cells[cell_x])):
            draw_cell = [(cell_x * tile_size + 1, cell_y * tile_size + 1),
                         ((cell_x + 1) * tile_size - 1), ((cell_y + 1) * tile_size - 1)]
            square = ImageDraw.Draw(frames[frame])
            colour = active_color if cells[cell_x][cell_y] else inactive_color
            square.rectangle(draw_cell, fill=colour)

    old_cells = deepcopy(cells)
    cells = calc_new_state()
    if cells == old_cells:
        print("Frames are the same, stopping.")
        break

# render the gif with all created frames.
frames[0].save(out_location, save_all=True, append_images=frames[1:],
               optimize=True, loop=loop_gif, duration=frame_delay)
