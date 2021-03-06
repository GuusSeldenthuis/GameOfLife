#!/bin/python3

from PIL import Image, ImageDraw
from copy import deepcopy
import csv

""""
SETTINGS, GLHF.
"""
tile_size = 25  # How big in px are the tiles. (25x25 for example)
# max frames -1 for rendering untill no change. (10000 when -1 to avoid endless loop.)
max_frames = 2
background_color = "#222"  # Tile-frame/background color.
inactive_color = "#000"  # Inactive tile color.
active_color = "#fff"  # Inactive tile color.
height = 4  # Horizonal cells (Set to 0 if it should be the cvs' max-height).
width = 4 # Vertical cells (Set to 0 if it should be the cvs' max-width).
# Your comma seperated values file. (Used as source for initial state)
csv_source = "./examples/blinker.csv"
out_location = "./examples/blinker.gif"  # Location of the outputted .gif file.
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
content = list(csv.reader(open(csv_source)))
content_height, content_width = len(content), len(content[0])
# Decide the map's height and width.
print("Before: %i, %i." % (len(content), len(content[0])))

if ((height > 0 or width > 0) and (content_height < height or content_width < width)):
    cells = [[None for i in range(width)] for j in range(height)]
    for row in range(len(content)):
        for column in range(len(content[row])):
            cells[row][column] = content[row][column]
else:
    cells = content

h, w = len(cells), len(cells[0])
print(cells)
print("Rendering GIF with height: %i and width: %i." % (h, w))
old_cells = deepcopy(cells)

frames = []
for_frames = 10000 if max_frames < 0 else max_frames
for frame in range(for_frames):
    # PIL accesses images in Cartesian co-ordinates, so it is Image[columns, rows]
    frames.append(Image.new('RGB', ((tile_size * w) + 1,
                  ((tile_size * h) + 1)), background_color))
    pixels = frames[frame].load()  # create the pixel map

    for row in range(len(cells)):
        for column in range(len(cells[row])):
            draw_cell = [
                (column * tile_size, row * tile_size),
                (column * tile_size + tile_size, row * tile_size + tile_size)
            ]
            square = ImageDraw.Draw(frames[frame])
            colour = active_color if cells[row][column] else inactive_color
            square.rectangle(draw_cell, fill=colour, outline=background_color)

    old_cells = deepcopy(cells)
    cells = calc_new_state()
    if cells == old_cells:
        print("Frames are the same, stopping.")
        break

# render the gif with all created frames.
frames[0].save(out_location, save_all=True, append_images=frames[1:],
               optimize=True, loop=loop_gif, duration=frame_delay)

print("Saved outputted GIF to: %s" % out_location)
