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

# # generate a histogram with the threshold range for an optimal bitmask
# histogram, bin_edges = np.histogram(blurred_img, bins=256, range=(0.0, 1.0))
# fig, ax = plt.subplots()
# plt.plot(bin_edges[0:-1], histogram)
# plt.title("Graylevel histogram")
# plt.xlabel("gray value")
# plt.ylabel("pixel count")
# plt.xlim(0, 1.0)


# using otsu's method, find the threshold value that best 'fits' for image segementation
# use the binary_mask to select the "interesting" part of the image
t = filters.threshold_otsu(blurred_img)
# yen's method for calculating thresholds
y = filters.threshold_yen(blurred_img)

# try all filters
fig, ax = filters.try_all_threshold(blurred_img, figsize=(20,18), verbose=False)
plt.savefig('../../Desktop/try_all.png', transparent=True)

print(f"threshold found at value: {t}")
# for all pixels greater than the predicted threshold value, keep them 'turned on'
binary_mask = blurred_img > t 

labeled_image, cell_count = measure.label(binary_mask, connectivity=2, return_num=True)
# remove one object for otsu as it is counting the background as an object
cell_count_otsu = (cell_count - 1)
print(f"There are {cell_count_otsu} cells in {path}")

# make a copy of the image
selection = image.copy()
# for all pixels that did not fit the criteria, set the value to 0 or 'turned off'
selection[~binary_mask] = 0
# display the combined image(bitmask and original image) without a grayscale filter applied
# fig, ax = plt.subplots()
# plt.imshow(selection)
# plt.show()

labeled_image, cell_count = measure.label(binary_mask, connectivity=2, return_num=True)
# store the data of from the mask application in the variable colored_label_image
colored_label_image = color.label2rgb(labeled_image)
# remove the grayscale filter
summary_image = color.gray2rgb(gray_img)
# apply the mask data to the numpy pixel array for printing
summary_image[binary_mask] = colored_label_image[binary_mask]
############################################################################


print(f"threshold found at value: {y}")
# create a second mask using yen's threshold value
binary_mask2 = blurred_img > y 
# create an image copy for the bitmask to be overlayed
selection2 =  image.copy()
# all pixels that do not meet the criteria are updated to 0's
selection2[~binary_mask2] = 0

labeled_image2, cell_count2 = measure.label(binary_mask2, connectivity=2, return_num=True)
print(f"There are {cell_count2} cells in {path}")

# store the data of from the mask application in the variable colored_label_image
colored_label_image2 = color.label2rgb(labeled_image2, bg_label=0)
# remove the grayscale filter
summary_image2 = color.gray2rgb(gray_img)
# apply the mask data to the numpy pixel array for printing
summary_image2[binary_mask2] = colored_label_image2[binary_mask2]

# print a figure for comparison purposes
# display images
fig = plt.figure(figsize=(14,12))
# plt.subplots_adjust(right=0.7)
rows=2
cols=3

fig.add_subplot(rows, cols, 1)
# display original image
plt.imshow(og_img)
plt.axis('on')
# plt.colorbar()
plt.title('Specimen #1\n Frame 1 of 97\n Z-pos: 01')

fig.add_subplot(rows, cols, 2)
plt.imshow(image)
plt.axis('on')
plt.title('Specimen #1\nGreen Channel Isolated')

fig.add_subplot(rows, cols, 3)
plt.imshow(binary_mask, cmap="gray")
plt.axis('on')
plt.title('Otsu Thresholding Method Bitmask')

fig.add_subplot(rows, cols, 4)
plt.imshow(summary_image)
plt.axis('on')
plt.title(f'Otsu Bitmask Applied to Image\nCell Count: {cell_count_otsu}')

fig.add_subplot(rows, cols, 5)
plt.imshow(binary_mask2, cmap="gray")
plt.axis('on')
plt.title('Yen Thresholding Method Bitmask')

fig.add_subplot(rows, cols, 6)
plt.imshow(summary_image2)
plt.axis('on')
plt.title(f'Yen Bitmask Applied to Image\nCell Count: {cell_count2}')
plt.savefig('../../Desktop/compare.png', transparent=True)

# 
# fig, ax = plt.subplots()
# plt.imshow(selection)