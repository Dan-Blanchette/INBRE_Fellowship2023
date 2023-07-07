"""
AUTHOR: Daniel Blanchette

DATE: July 5 2023

DESCRIPTION: This program will batch process Z-stacks in each frame folder and apply the
Otsu + Multi-Otsu methods for image segmentation and quantification.
"""
import pandas as pd
import csv
from skimage import io
import os
import numpy as np
import glob
import matplotlib.pyplot as plt
import ipympl
import cv2
import re
import numpy as np
# import imageio.v3 as iio
from skimage import color
from skimage import filters
from skimage import measure
from skimage import img_as_ubyte

image_list = []

# select the path
path1 = "../../Desktop/greenImgs/spec_1/frame_1/*.tif"
path2 = "../../Desktop/greenImgs/spec_1/frame_2/*.tif"
path3 = "../../Desktop/greenImgs/spec_1/frame_3/*.tif"
path4 = "../../Desktop/greenImgs/spec_1/frame_4/*.tif"
path5 = "../../Desktop/greenImgs/spec_1/frame_5/*.tif"

path_list = [path1, path2, path3, path4, path5]

# create a dictionary for printing out a .csv file with results


img_number = 1  # Start an iterator for image number.
# This number can be later added to output image file names.


for i in range(5):
    print(f'Frame_{i+1} Batch')
    with open(f'../../Desktop/batch2_files/FR{i+1}_YenOtsu_Results.csv', 'w', newline='') as csvfile:
        fieldnames = ['Frame_ID', 'Z-pos', 'Cell_Count',
            'Thresh_Method', 'Threshold Val']
        my_writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        my_writer.writeheader()
    
        # sort
        for file in sorted(glob.glob(path_list[i])):
            print(file)     # check path is being processed in order
            img = io.imread(file, plugin='pil')
            # plt.imshow(img)
            # plt.show()
            gray_img = color.rgb2gray(img)
            blurred_img = filters.gaussian(gray_img, sigma=1.5)
            # plt.imshow(blurred_img)
            # plt.show()
            yen_thresh = filters.threshold_yen(blurred_img)
            mult_ot_thresh = filters.threshold_multiotsu(blurred_img, 5)
            # plt.savefig(f'../../Desktop/batch_files/{img_number}_RES.png', dpi=300)
            # the minimum threshold value based on multi-otsu
            min_val = float(mult_ot_thresh[0])
            # the best predicted median value based on the multi-otsu
            mot_med1 = float(mult_ot_thresh[1])
            # median value 2
            mot_med2 = float(mult_ot_thresh[2])
            # the largest possible predicted value for the image multi-otsu
            max_value = float(mult_ot_thresh[3])

            # ************** DARKER IMAGES ********************
            '''if the otsu threshold predicted is greater than the min mult-otsu value
                    and the second highest value is less than 0.09'''
            if (min_val < yen_thresh) and (mot_med2 < 0.09):
                    '''The image is darker in contrast so use the adjusted max threhold value
                    for segmentation
                    '''
                    if (max_value > 0.11 and mot_med2 < 0.09):
                        # this case chooses a hard value just under 0.1
                        # NOTE: in observed runs of the program, optimal values were between
                        # 0.089 and 0.11. this ensures for darker images that cells
                        # have a chance to be picked up
                        adj_max = 0.097
                        binary_mask = blurred_img > adj_max
                        chosen_thresh = adj_max
                        thresh_type = "Adj_Max_Thresh"
                    else:
                        # otherwise default to the max value predicted
                        binary_mask = blurred_img > max_value
                        chosen_thresh = max_value
                        thresh_type = "mot_Max_Thresh"
    
                    # print(f'{thresh_type} {round(chosen_thresh,3)} applied to Z{img_number}')
    
            # ******************* EDGE CASE WHERE MULTI-OTSU VALUE IN LIST ELEMENT 1 IS JUST ABOVE 0.1 ***********
                    '''else if the otsu thresh is greater than the min mult-otsu value
                        and the second lowest multi-otsu value is less than the
                        otsu threhsold and the same second lowest value is greater than 0.1'''
            elif (min_val < yen_thresh) and (mot_med1 < yen_thresh) and (mot_med1 > 0.1):
                    '''use the second lowest value from mult-otsu as a threshold'''
                    binary_mask = blurred_img > mot_med1
                    chosen_thresh = mot_med1
                    thresh_type = "M_Ot_med1 Thresh"
                    # print(f'Med-1 Value {mot_med1} applied to Z{img_number} ')
    
            # ************ EDGE CASE WHERE THE OTSU THREHSHOLD WILL BE USED  **********
            # else if the min_val multi-tosu is less than the otsu threshold
            # and the otsu threshold is still less than the max_value for multi-otsu
            elif (min_val < yen_thresh) and (yen_thresh < max_value):
                    # use the otsu threhold in this case
                    if yen_thresh > 0.2:
                        binary_mask = blurred_img > mot_med2
                        chosen_thresh = mot_med2
                        thresh_type = "mod_med2 Thresh"
                    else:
                        binary_mask = blurred_img > yen_thresh
                        chosen_thresh = yen_thresh
                        thresh_type = "Yen Thresh"
    

                    print(f'Using {thresh_type} {chosen_thresh} applied to Z{img_number} ')
            # ************ DEFAULT TO THE MULTI-OTSU VALUE THAT IS ONE ABOVE THE MIN VALUE ***************
            else:
                # otherwise, use the second lowest image segmentation for all other cases.
                if mot_med1 > 0.085:
                    binary_mask = blurred_img > mot_med1
                    chosen_thresh = mot_med1
                    thresh_type = "Def: mot med1 Thresh"
                    # print(f'Defaulting to Med1_Value {mot_med1} applied to Z{img_number} ')
                else:
                     binary_mask = blurred_img > mot_med2
                     chosen_thresh = mot_med2
                     thresh_type = "Def: mot med2 Thresh"
    
            labeled_image, cell_count = measure.label(binary_mask, connectivity=2, return_num=True)
            # remove one object for otsu as it is counting the background as an object
    
            # make a copy of the image
            selection = img.copy()
            # for all pixels that did not fit the criteria, set the value to 0 or 'turned off'
            selection[~binary_mask] = 0
            # display the combined image(bitmask and original image) without a grayscale filter applied
            # fig, ax = plt.subplots()
            # plt.imshow(selection)
            # plt.show()
    
            labeled_image, cell_count = measure.label(
                binary_mask, connectivity=1, return_num=True)
            # store the data of from the mask application in the variable colored_label_image
            colored_label_image = color.label2rgb(labeled_image)
            # remove the grayscale filter
            summary_image = color.gray2rgb(gray_img)
            # apply the mask data to the numpy pixel array for printing
            summary_image[binary_mask] = colored_label_image[binary_mask]
            # print(f"There are {cell_count} cells in {path1}")
    
            # matplotlib.rc('font', **font)
            fig = plt.figure(figsize=(10, 7))
            rows = 1
            cols = 3
    
            #  *********** GREEN CHANNEL IMAGE ***************
    
            fig.add_subplot(rows, cols, 1)
            fig.tight_layout()
            plt.imshow(img)
            plt.axis('off')
            plt.title(f'Specimen #1\nGr_Chan_Z{img_number}\nFrame_{i+1}', fontsize=14)

    
            # ************* OTSU BITMASK OUTPUT *************
            fig.add_subplot(rows, cols, 2)
            plt.imshow(binary_mask, cmap="gray")
            plt.axis('off')
            plt.title(f'{thresh_type}\nThresh_Val: {round(chosen_thresh, 3)}', fontsize=14)

            
            fig.add_subplot(rows, cols, 3)
            plt.imshow(summary_image)
            plt.axis('off')
            plt.title(f'Applied {thresh_type}\nCell Count: {cell_count}', fontsize=14)
            
            plt.savefig(f'../../Desktop/batch2_files/FR{i+1}_Z{img_number}_YenOtsu_Results.png', dpi=300)
            # plt.show()
            plt.close(fig)
    
            # Create a .csv file with counts recorded for the batch
    
            my_writer.writerow({'Frame_ID': f'{i+1}', 'Z-pos': img_number,
                                'Cell_Count': cell_count, 
                                'Thresh_Method': thresh_type, 
                                'Threshold Val': round(chosen_thresh, 3)
                                })
    

            if (img_number % 19 == 0):
                img_number = 1
            else:
                img_number += 1           
    csvfile.close()