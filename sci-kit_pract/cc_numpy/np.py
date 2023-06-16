from skimage import data
import numpy as np
import matplotlib.pyplot as plt

camera = data.camera()

print(type(camera))

# getting the total number of pixels from the image

# image dimensions
print(camera.shape)
# total pixles
print(camera.size)

# getting statistical information about the image intensity values
print(camera.min(), camera.max())
print(camera.mean())

print(len(camera))
print(camera[10, 20])

camera[3, 10] = 0
print(camera[3, 10])

# slicing with numpy

'''set the first ten lines to black'''
camera[:10] = 0
print(camera[:10])

'''creating a bit mask'''
mask = camera < 87
# set the pixels to white where the logic is true
camera[mask] = 255

inds_r = np.arange(len(camera))
inds_c = 4 * inds_r % len(camera)
camera[inds_r, inds_c] == 0

nrows, ncols = camera.shape
row, col = np.ogrid[:nrows, :ncols]
cnt_row, cnt_col = nrows / 2, ncols / 2

outer_disk_mask = ((row -cnt_row) **2 + (col - cnt_col) **2 > (nrows / 2 ) **2)

camera[outer_disk_mask] = 0

    