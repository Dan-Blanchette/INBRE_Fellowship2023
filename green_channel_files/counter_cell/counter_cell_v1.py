#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 22 14:52:58 2022

@author: Dan Blanchette

References:
1. Meysenburg, Mark. “Image Processing with Python.” Data Carpentry,	
   https://datacarpentry.org/image-processing/. Accessed  7 June 2022.


Copyright (c) 2002, Daniel Blanchette
All rights reserved.

This source code is licensed under the BSD-style license found in the
LICENSE file in the root directory of this source tree. 
"""

import matplotlib.pyplot as plt
import skimage.io as io
from glob import glob
import os.path as osp# future integration with the command line
import skimage.filters
import skimage.color
import skimage.measure
from PIL.Image import core as imaging


# this fucntion produces three images across the pixel channel spectrum
# def rgb_splitter(image):
#     rgb_list = ['Reds', 'Greens', 'Blues']
#     fig, ax = plt.subplots(1, 3, figsize=(15,5), sharey=True)
#     for i in range(3):
#         ax[i].imshow(image[:,:,i], cmap = rgb_list[i])
#         ax[i].set_title(rgb_list[i], fontsize = 15)


    

# prints original image plot to notebook/photoviewer
# and returns the file read variable to be used in other functions
def show_img(image):
    new_img = io.imread(image, plugin='pil')
    plt.imshow(new_img)
    # plt.axis('off')
    plt.show()
    return new_img

# Isolates the microglia cells based on thresholded values of the RGB channels
# and gererates a modified copy of the original image with only the 
# microglia cells being identified.
def cells_only(image_path, connectivity = 2, count = 1):
    img1 = show_img(image_path)
    # Green channel bit mask applied
    green_filtered_cells = (img1[:,:,1] > 132) & (img1[:,:,0] <= 97) & (img1[:,:,2] <= 97)
    # make a copy of the original image
    cells_new = img1.copy()
    # for all color channels (numpy arrays), apply the bit mask logic
    cells_new[:,:,0] = cells_new[:,:,0] * green_filtered_cells
    cells_new[:,:,1] = cells_new[:,:,1] * green_filtered_cells
    cells_new[:,:,2] = cells_new[:,:,2] * green_filtered_cells
    # convert the bit masked image to grayscale.
    gray_cells = skimage.color.rgb2gray(cells_new)
    # apply gaussian blur to further eliminate background noise from the image.
    blurred_image = skimage.filters.gaussian(gray_cells, sigma = 3.0)
    # store the new mask value with a gray scale threshold to improve cell count in variable 'mask'
    mask = blurred_image > 0.1
    # apply color fill
    labeled_image, cell_count = skimage.measure.label(mask, connectivity=connectivity, return_num=True)
    # console print out of identfied cell counts based on the applied mask
    print(f"There are {cell_count} cells in {image_path}")
    
    # store the data of from the mask application in the variable colored_label_image
    colored_label_image = skimage.color.label2rgb(labeled_image, bg_label=0)
    # remove the grayscale filter
    summary_image = skimage.color.gray2rgb(gray_cells)
    # apply the mask data to the numpy pixel array for printing
    summary_image[mask] = colored_label_image[mask]
    
    # OPTIONAL SETTINGS FOR IMAGE RESIZING
    # plt.figure(num=None, figsize=(8, 6), dpi=80, facecolor='none', clear=True)
    # plt.box(on=None)
    # plt.axis('off')

    # display each image and as a return the settings for the summary_image
    plt.imshow(summary_image)
    plt.show()
    return summary_image 