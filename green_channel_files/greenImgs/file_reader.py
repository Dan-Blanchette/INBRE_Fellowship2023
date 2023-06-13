from skimage import io
import os
import numpy as np
import glob
import matplotlib.pyplot as plt
import ipympl
import imageio.v3 as iio
from skimage import color
from skimage import filters
from skimage import measure


current_dir = os.getcwd()
# print(current_dir)

path = str(current_dir) + "/frames_1/013020_Lgalsbpb_GFPpos_NoTreatment_T01_XY1_Z10_RGB_Green.tif"

# print(path)
im = io.imread(path, plugin='pil')

gray_img = color.rgb2gray(im)

blurred_img = filters.gaussian(gray_img, sigma=1.0)

fig, ax = plt.subplots()

# imarray = np.array(im)

# print(imarray.shape)
# print(imarray.size)
# print(imarray)
plt.imshow(blurred_img, cmap='gray')

# create a mask based on the threshold
t = 0.1
binary_mask = blurred_img < t

fig, ax = plt.subplots()
plt.imshow(binary_mask, cmap="gray")

# create a histogram of the blurred grayscale image
histogram, bin_edges = np.histogram(blurred_img, bins=256, range=(0.0, 1.0))

fig, ax = plt.subplots()
plt.plot(bin_edges[0:-1], histogram)
plt.title("Grayscale Histogram")
plt.xlabel("grayscale value")
plt.ylabel("pixels")
plt.xlim(0, 1.0)


# automatic thresholding tests

path = str(current_dir) + "/frames_1/013020_Lgalsbpb_GFPpos_NoTreatment_T01_XY1_Z10_RGB_Green.tif"

# print(path)
im = io.imread(path, plugin='pil')

fig, ax = plt.subplots()
plt.imshow(im)

# convert the image to grayscale
gray_image = color.rgb2gray(im)

# blur the image to denoise
blurred_image = filters.gaussian(gray_image, sigma=1.0)

# show the histogram of the blurred image
histogram, bin_edges = np.histogram(blurred_image, bins=256, range=(0.0, 1.0))
fig, ax = plt.subplots()
plt.plot(bin_edges[0:-1], histogram)
plt.title("Graylevel histogram")
plt.xlabel("gray value")
plt.ylabel("pixel count")
plt.xlim(0, 1.0)

# use the binary_mask to select the "interesting" part of the image
selection = im.copy()
selection[~binary_mask] = 0

fig, ax = plt.subplots()
plt.imshow(selection)

# perform automatic thresholding
t = filters.threshold_otsu(blurred_image)
print("Found automatic threshold t = {}.".format(t))

# create a binary mask with the threshold found by Otsu's method
binary_mask = blurred_image > t

fig, ax = plt.subplots()
plt.imshow(binary_mask, cmap="gray")

# apply the binary mask to select the foreground
selection = im.copy()
selection[~binary_mask] = 0


# display images
fig = plt.figure(figsize=(10,7))
plt.subplots_adjust(right=0.6)
rows=2
cols=2

fig.add_subplot(rows, cols, 1)
# display original image
plt.imshow(im)
plt.axis('on')
plt.title('Specimen #1\n Frame 1 of 97\n Z-pos: 10')

fig.add_subplot(rows, cols, 2)
# display original image
plt.imshow(binary_mask, cmap="gray")
plt.axis('on')
plt.title('otsu bitmask')

fig.add_subplot(rows, cols, 3)
# display original image
plt.imshow(selection)
plt.axis('on')
plt.title('bitmask applied to Image')

#
fig, ax = plt.subplots()
plt.imshow(selection)


labeled_image, cell_count = measure.label(selection, connectivity=2, return_num=True)

print(f"There are {cell_count} cells in {path}")

colored_label_image = color.label2rgb(labeled_image, bg_label=0)

summary_image = color.gray2rgb(gray_image)

summary_image[selection] = colored_label_image[selection]

plt.imshow(summary_image)
plt.show()
