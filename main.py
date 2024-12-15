#!/bin/python3

from PIL import Image, ImageDraw
import csv

""""
SETTINGS, GLHF.
"""
tile_size = 10  # How big in px are the tiles. (25x25 for example)
# max frames -1 for rendering untill no change. (10000 when -1 to avoid endless loop.)
max_frames = 30  # Changed to 2 since we only need two states for the blinker
background_color = "#000"  # Tile-frame/background color.
inactive_color = "#010"  # Inactive tile color.
active_color = "#0f0"  # Inactive tile color.
height = 10  # Horizonal cells (Set to 0 if it should be the cvs' max-height).
width = 10 # Vertical cells (Set to 0 if it should be the cvs' max-width).
# Your comma seperated values file. (Used as source for initial state)
csv_source = "./examples/glider.csv"
out_location = "./examples/glider.gif"  # Location of the outputted .gif file.
frame_delay = 100  # Amount of ms between frames.
loop_gif = 1  # Set to False to no-loop gif.
""""
END OF SETTINGS.
"""


# 'Safe' way to check for active neighbors despite being outside of the matrix.
def is_active(cells, x, y):
    try:
        if x < 0 or y < 0:  # Explicitly check for negative indices
            return False
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
def calc_new_state(current_cells):
    new_cells = [[False for _ in range(len(current_cells[0]))] for _ in range(len(current_cells))]
    for cur_cell_x in range(len(current_cells)):
        for cur_cell_y in range(len(current_cells[cur_cell_x])):
            neighbors = amount_of_neighbors(current_cells, cur_cell_x, cur_cell_y)
            current_state = current_cells[cur_cell_x][cur_cell_y]
            
            # Rule 1: Any live cell with fewer than two live neighbors dies (underpopulation)
            # Rule 2: Any live cell with two or three live neighbors lives on to the next generation
            # Rule 3: Any live cell with more than three live neighbors dies (overpopulation)
            # Rule 4: Any dead cell with exactly three live neighbors becomes a live cell (reproduction)
            if current_state and neighbors in [2, 3]:
                new_cells[cur_cell_x][cur_cell_y] = True
            elif not current_state and neighbors == 3:
                new_cells[cur_cell_x][cur_cell_y] = True
    return new_cells


# Do loading n' stuff.
content = list(csv.reader(open(csv_source)))
content_height, content_width = len(content), len(content[0])
# Convert CSV content to boolean values
content = [[cell == 'x' for cell in row] for row in content]

# Decide the map's height and width.
print("Before: %i, %i." % (len(content), len(content[0])))

if ((height > 0 or width > 0) and (content_height < height or content_width < width)):
    cells = [[False for i in range(width)] for j in range(height)]
    for row in range(len(content)):
        for column in range(len(content[row])):
            cells[row][column] = content[row][column]
else:
    cells = content

h, w = len(cells), len(cells[0])
print("Initial state:")
for row in cells:
    print(['x' if cell else '.' for cell in row])
print("Rendering GIF with height: %i and width: %i." % (h, w))

frames = []
current_state = cells
for frame in range(max_frames):
    print(f"\nFrame {frame}:")
    for row in current_state:
        print(['x' if cell else '.' for cell in row])
        
    # PIL accesses images in Cartesian co-ordinates, so it is Image[columns, rows]
    frames.append(Image.new('RGB', (tile_size * w,
                  tile_size * h), background_color))
    pixels = frames[frame].load()  # create the pixel map

    for row in range(len(current_state)):
        for column in range(len(current_state[row])):
            draw_cell = [
                (column * tile_size, row * tile_size),
                (column * tile_size + tile_size - 1, row * tile_size + tile_size - 1)
            ]
            square = ImageDraw.Draw(frames[frame])
            colour = active_color if current_state[row][column] else inactive_color
            square.rectangle(draw_cell, fill=colour, outline=background_color)

    current_state = calc_new_state(current_state)

# render the gif with all created frames.
frames[0].save(out_location, save_all=True, append_images=frames[1:],
               optimize=True, loop=loop_gif, duration=frame_delay)

print("Saved outputted GIF to: %s" % out_location)
