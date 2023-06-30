from skimage import io
import os
import numpy as np
import statistics as stats
import glob
import matplotlib
import matplotlib.pyplot as plt
import ipympl
# import imageio.v3 as iio
from skimage import color
from skimage import filters
from skimage import measure

# provide the file path to the original
original_img = "../../Desktop/rgbFiles/spec_1/frame_1/013020_Lgalsbpb_GFPpos_NoTreatment_T01_XY1_Z03_RGB.tif"
og_img = io.imread(original_img, plugin='pil')
# plt.imshow(og_img)
# plt.show()


# green channel only image
path = "../../Desktop/greenImgs/spec_1/frame_1/013020_Lgalsbpb_GFPpos_NoTreatment_T01_XY1_Z03_RGB_Green.tif"

image = io.imread(path, plugin='pil')

# plt.imshow(image)
# plt.show()

# convert the image to grayscale
gray_img = color.rgb2gray(image)
blurred_img = filters.gaussian(gray_img, sigma=1.5)
# plt.imshow(blurred_img, cmap='gray')
# plt.show()


# ************************** OTSU's METHOD ************************************
# using otsu's method, find the threshold value that best 'fits' for image segementation
# use the binary_mask to select the "interesting" part of the image
ot_thresh = filters.threshold_otsu(blurred_img)
# ************************** MULTI OTSU's METHOD ************************************
# using multi-otsu's method, find the threshold value that best 'fits' for image segementation
# use the binary_mask to select the "interesting" part of the image
mult_ot_thresh = filters.threshold_multiotsu(blurred_img, 5)
print(mult_ot_thresh, ot_thresh)
# the minimum threshold value based on multi-otsu
min_val =  float(mult_ot_thresh[0])
# the best predicted median value based on the multi-otsu
mot_med1 = float(mult_ot_thresh[1])
# median value 2
mot_med2 = float(mult_ot_thresh[2])
# the largest possible predicted value for the image multi-otsu
max_value = float(mult_ot_thresh[3])
# print(f"threshold found at value: {float(mult_ot_thresh[1])}")
print(min_val, mot_med1, max_value, ot_thresh)

#  binary_mask = blurred_img > max_value
# if the threshold predicted is greater than the min mult-otsu value
if (min_val < ot_thresh) and (mot_med2 < 0.09):
    binary_mask = blurred_img > max_value
    chosen_thresh = max_value
elif (min_val < ot_thresh) and (mot_med1 < ot_thresh) and (mot_med1 > 0.1):
    binary_mask = blurred_img > mot_med1
    chosen_thresh = mot_med1
elif (min_val < ot_thresh) and (ot_thresh < max_value):
    binary_mask = blurred_img > ot_thresh
    chosen_thresh = ot_thresh
else:
    binary_mask = blurred_img > mot_med1
    chosen_thresh = mot_med1

# # for all pixels greater than the predicted threshold value, keep them 'turned on'
# binary_mask = blurred_img > default




labeled_image, cell_count = measure.label(binary_mask, connectivity=2, return_num=True)
# remove one object for otsu as it is counting the background as an object


# make a copy of the image
selection = image.copy()
# for all pixels that did not fit the criteria, set the value to 0 or 'turned off'
selection[~binary_mask] = 0
# display the combined image(bitmask and original image) without a grayscale filter applied
# fig, ax = plt.subplots()
# plt.imshow(selection)
# plt.show()

labeled_image, cell_count = measure.label(binary_mask, connectivity=1, return_num=True)
# store the data of from the mask application in the variable colored_label_image
colored_label_image = color.label2rgb(labeled_image)
# remove the grayscale filter
summary_image = color.gray2rgb(gray_img)
# apply the mask data to the numpy pixel array for printing
summary_image[binary_mask] = colored_label_image[binary_mask]
print(f"There are {cell_count} cells in {path}")


# matplotlib.rc('font', **font)
fig = plt.figure(figsize=(12,12))
rows=1
cols=3


# *********** GREEN CHANNEL IMAGE ***************

fig.add_subplot(rows, cols, 1)
fig.tight_layout(pad=7.0)
plt.imshow(image)
plt.axis('off')
plt.title('Specimen #1\nGreen Channel Isolated', fontsize = 18)

# ************* OTSU BITMASK OUTPUT *************
fig.add_subplot(rows, cols, 2)
plt.imshow(binary_mask, cmap="gray")
plt.axis('off')
plt.title(f'Otsu Bitmask\nThresh_Val: {round(chosen_thresh, 3)}', fontsize = 18)

fig.add_subplot(rows, cols, 3)
plt.imshow(summary_image)
plt.axis('off')
plt.title(f'Otsu Bitmask Applied to Image\nCell Count: {cell_count}', 
          fontsize = 18)