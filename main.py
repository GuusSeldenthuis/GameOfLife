#!/bin/python3

from PIL import Image
import random

images = []

for x in range(10):
	# PIL accesses images in Cartesian co-ordinates, so it is Image[columns, rows]
	images.append(Image.new( 'RGB', (1000,1000), "black")) # create a new black image
	pixels = images[x].load() # create the pixel map

	for i in range(images[x].size[0]):    # for every col:
	    for j in range(images[x].size[1]):    # For every row
	        pixels[i,j] = (x * 25, j * 10, i * 10) # set the colour accordingly

# img.save("image.jpg", "JPEG")
images[0].save('out.gif', save_all=True, append_images=images[1:], optimize=True, loop=0)
