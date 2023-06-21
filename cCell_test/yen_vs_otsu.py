from skimage import io
import os
import numpy as np
import glob
import matplotlib.pyplot as plt
import ipympl
# import imageio.v3 as iio
from skimage import color
from skimage import filters
from skimage import measure

# provide the file path to the original
original_img = "../../Desktop/rgbFiles/spec_1/frame_1/013020_Lgalsbpb_GFPpos_NoTreatment_T01_XY1_Z02_RGB.tif"
og_img = io.imread(original_img, plugin='pil')
# plt.imshow(og_img)
# plt.show()


# green channel only image
path = "../../Desktop/greenImgs/spec_1/frame_1/013020_Lgalsbpb_GFPpos_NoTreatment_T01_XY1_Z02_RGB_Green.tif"

image = io.imread(path, plugin='pil')

# plt.imshow(image)
# plt.show()

# convert the image to grayscale
gray_img = color.rgb2gray(image)
blurred_img = filters.gaussian(gray_img, sigma=1.0)
# plt.imshow(blurred_img, cmap='gray')
# plt.show()

# generate a histogram with the threshold range for an optimal bitmask
histogram, bin_edges = np.histogram(blurred_img, bins=256, range=(0.0, 1.0))
fig, ax = plt.subplots()
plt.plot(bin_edges[0:-1], histogram)
plt.title("Graylevel histogram")
plt.xlabel("gray value")
plt.ylabel("pixel count")
plt.xlim(0, 1.0)


# using otsu's method, find the threshold value that best 'fits' for image segementation
# use the binary_mask to select the "interesting" part of the image
t = filters.threshold_otsu(blurred_img)
# yen's method for calculating thresholds
y = filters.threshold_yen(blurred_img)

# try all filters
all_thresh = filters.try_all_threshold(blurred_img)

tri = filters.threshold_triangle(blurred_img)
print(f"threshold found at value: {t}")
# for all pixels greater than the predicted threshold value, keep them 'turned on'
binary_mask = blurred_img > t
# make a copy of the image
selection = image.copy()
# for all pixels that did not fit the criteria, set the value to 0 or 'turned off'
selection[~binary_mask] = 0
# display the combined image(bitmask and original image) without a grayscale filter applied
# fig, ax = plt.subplots()
# plt.imshow(selection)
# plt.show()


binary_mask2 = blurred_img > y 

selection2 =  image.copy()

selection2[~binary_mask2] = 0


# print a figure for comparison purposes
# display images
fig = plt.figure(figsize=(17,15))
plt.subplots_adjust(right=0.9)
rows=3
cols=3

fig.add_subplot(rows, cols, 1)
# display original image
plt.imshow(og_img)
plt.axis('on')
plt.title('Specimen #1\n Frame 1 of 97\n Z-pos: 02')

fig.add_subplot(rows, cols, 2)
# display original image
plt.imshow(image)
plt.axis('on')
plt.title('Green Channel Image')

fig.add_subplot(rows, cols, 3)
# display original image
plt.imshow(binary_mask, cmap="gray")
plt.axis('on')
plt.title('otsu bitmask')

fig.add_subplot(rows, cols, 4)
# display original image
plt.imshow(selection)
plt.axis('on')
plt.title('Otsu bitmask applied to Image')

fig.add_subplot(rows, cols, 5)
# display original image
plt.imshow(binary_mask2, cmap="gray")
plt.axis('on')
plt.title('Yen bitmask applied to Image')

fig.add_subplot(rows, cols, 6)
# display original image
plt.imshow(selection2)
plt.axis('on')
plt.title('Yen bitmask applied to Image')


# 
# fig, ax = plt.subplots()
# plt.imshow(selection)