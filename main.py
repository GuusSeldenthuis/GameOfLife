#!/bin/python3

from PIL import Image, ImageDraw
import random

init_state = "     " + \
			 "  #  " + \
			 "  #  " + \
			 "  #  " + \
			 "     "


def make_cells(init_state):
	w, h = 5, 5
	i, j = 0, 0
	new_cells = [[0 for x in range(w)] for y in range(h)]
	for char in range(0, len(init_state)):
		new_cells[i][j] = True if init_state[char] == " " else False

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

# cells[0][0] = True
# cells[0][1] = True
# cells[0][2] = True
# cells[0][3] = True
# cells[0][4] = True
# cells[0][5] = True


# DRAW PIXELS
images = []
# 10 frames to render.
for frame in range(1):
	# PIL accesses images in Cartesian co-ordinates, so it is Image[columns, rows]
	images.append(Image.new( 'RGB', (250,250), "black")) # create a new black image
	pixels = images[frame].load() # create the pixel map
	
	x, y = 0, 0
	for row in cells:
		x = 0
		for cell in row:
			draw_cell = [(50, 50), (x * 50, y * 50)]
			# create rectangle image
			img1 = ImageDraw.Draw(images[frame])
			print("[" + str(x) + "][" + str(y) + "]: " + str(cells[x][y]))
			img1.rectangle(draw_cell, fill = "#ffffff" if cells[x][y] else "#000000")
			x += 1
		y += 1

# img.save("image.jpg", "JPEG")
images[0].save('out.gif', save_all=True, append_images=images[1:], optimize=True, loop=0)
