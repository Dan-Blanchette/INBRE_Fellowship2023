"""
AUTHOR: Daniel Blanchette

DATE: July 5 2023
 
DESCRIPTION: This program will batch process Z-stacks in each frame folder and apply Yen or Triangle
then choose a value from the Multi-Otsu method for image segmentation and quantification.
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

image_list =[]

#select the path
path1 = "../../Desktop/greenImgs/spec_1/frame_1/*.tif"
path2 = "../../Desktop/greenImgs/spec_1/frame_2/*.tif"
path3 = "../../Desktop/greenImgs/spec_1/frame_3/*.tif"
path4 = "../../Desktop/greenImgs/spec_1/frame_4/*.tif"
path5 = "../../Desktop/greenImgs/spec_1/frame_5/*.tif"

# create a dictionary for printing out a .csv file with results



img_number = 1  #Start an iterator for image number.
#This number can be later added to output image file names.

with open('../../Desktop/batch_files/FR1_Tri_Otsu_Results.csv', 'w', newline='') as csvfile:
    # sort  
    for file in sorted(glob.glob(path1)):
        # print(file)     # check path is being processed in order
        img = io.imread(file, plugin='pil')
        # plt.imshow(img)
        # plt.show()
        gray_img = color.rgb2gray(img)
        blurred_img = filters.gaussian(gray_img, sigma=1.5)
        # plt.imshow(blurred_img)
        # plt.show()
        tri_thresh = filters.threshold_triangle(blurred_img)
        print(f'the triangle threshold value is: {tri_thresh}')
        
        yen_thresh = filters.threshold_yen(blurred_img)
        print(f'the yen threshold value is: {yen_thresh}')
        
        mult_ot_thresh = filters.threshold_multiotsu(blurred_img, 5)
        # plt.savefig(f'../../Desktop/batch_files/{img_number}_RES.png', dpi=300)
        # the minimum threshold value based on multi-otsu
        min_val =  float(mult_ot_thresh[0])
        # the best predicted median value based on the multi-otsu
        mot_med1 = float(mult_ot_thresh[1])
        # median value 2
        mot_med2 = float(mult_ot_thresh[2])
        # the largest possible predicted value for the image multi-otsu
        max_value = float(mult_ot_thresh[3])
        
        # ************** DARKER IMAGES ********************
        """if the otsu threshold predicted is greater than the min mult-otsu value
            and the second highest value is less than 0.09
        """
        if (min_val < tri_thresh) and (mot_med2 < 0.09):
            '''The image is darker in contrast so use the max threhold value
                for sementation
            '''   
            binary_mask = blurred_img > max_value
            chosen_thresh = max_value
            print(f'Max Value {max_value} applied to Z{img_number}' )
            

        # ******************* EDGE CASE WHERE MULTI-OTSU VALUE IN LIST ELEMENT 1 IS JUST ABOVE 0.1 ***********
        # else if the triangle threshold is greater than the min mult-otsu value 
        # and the second lowest multi-otsu value is less than the triangle threhsold 
        # and the same second lowest value is greater than 0.1      
        elif (min_val < tri_thresh) and (mot_med1 < tri_thresh) and (mot_med1 > 0.1):
            """use the second lowest value from mult-otsu as a threshold"""
            binary_mask = blurred_img > mot_med1
            chosen_thresh = mot_med1
            print(f'Med-1 Value {mot_med1} applied to Z{img_number} ')
    
        # ************ EDGE CASE WHERE THE OTSU THREHSHOLD WILL BE USED  **********
            '''else if the min_val multi-tosu is less than the otsu threshold
                and the otsu threshold is still less than the max_value for multi-otsu'''
        elif (min_val < tri_thresh) and (tri_thresh < max_value):
            # use the otsu threhold in this case
            binary_mask = blurred_img > tri_thresh
            chosen_thresh = tri_thresh
            print(f'Using Triangle Thresh Value {tri_thresh} applied to Z{img_number} ')
        # ************ DEFAULT TO THE MULTI-OTSU VALUE THAT IS ONE ABOVE THE MIN VALUE ***************
        else:
            # otherwise, use the second lowest image segmentation for all other cases.
            binary_mask = blurred_img > mot_med1
            chosen_thresh = mot_med1
            print(f'Defaulting to Med1_Value {mot_med1} applied to Z{img_number} ')
        
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
    
        labeled_image, cell_count = measure.label(binary_mask, connectivity=1, return_num=True)
        # store the data of from the mask application in the variable colored_label_image
        colored_label_image = color.label2rgb(labeled_image)
        # remove the grayscale filter
        summary_image = color.gray2rgb(gray_img)
        # apply the mask data to the numpy pixel array for printing
        summary_image[binary_mask] = colored_label_image[binary_mask]
        # print(f"There are {cell_count} cells in {path1}")
    
    
        # matplotlib.rc('font', **font)
        fig = plt.figure(figsize=(10,7))
        rows=1
        cols=3
    
    
        # *********** GREEN CHANNEL IMAGE ***************
    
        fig.add_subplot(rows, cols, 1)
        fig.tight_layout()
        plt.imshow(img)
        plt.axis('off')
        plt.title(f'Specimen #1\nGr_Chan_Z{img_number}\nFrame_1', fontsize = 14)
    
        # ************* OTSU BITMASK OUTPUT *************
        fig.add_subplot(rows, cols, 2)
        plt.imshow(binary_mask, cmap="gray")
        plt.axis('off')
        plt.title(f'Chosen Bitmask\nThresh_Val: {round(chosen_thresh, 3)}', fontsize = 14)
    
        fig.add_subplot(rows, cols, 3)
        plt.imshow(summary_image)
        plt.axis('off')
        plt.title(f'Chosen Bitmask Applied to Image\nCell Count: {cell_count}', 
                  fontsize = 14)
        
    
        cell_count_lst =[]
        cell_count_lst.append(cell_count)
        # Create a .csv file with counts recorded for the batch
        
        my_writer = csv.writer(csvfile, delimiter=' ')
        my_writer.writerow(cell_count_lst)
        
        
            
        # plt.savefig(f'../../Desktop/batch_files/FR1_Z{img_number}_Tri_Results.png', dpi=300)
        plt.show()
        plt.close(fig)
        img_number += 1
    
        # fig = plt.figure(figsize=(14,12))
        # # plt.subplots_adjust(right=0.7)
        # rows=2
        # cols=3
    
        # fig.add_subplot(rows, cols, 1)
        # # display original image
        # plt.imshow(og_img)
        # plt.axis('on')
        # # plt.colorbar()
        # plt.title('Specimen #1\n Frame 1 of 97\n Z-pos: 01')
    
        # fig.add_subplot(rows, cols, 2)
        # # display original image
        # plt.imshow(image)
        # plt.axis('on')
        # plt.title('Specimen #1\n Frame 1 of 97\n Z-pos: 02\n[Green Channel Isolated]')
    
        # fig.add_subplot(rows, cols, 3)
        # # display original image
        # plt.imshow(binary_mask, cmap="gray")
        # plt.axis('on')
        # plt.title('Otsu Thresholding Method Bitmask')
    
        # fig.add_subplot(rows, cols, 4)
        # # display original image
        # plt.imshow(summary_image)
        # plt.axis('on')
        # plt.title(f'Otsu Bitmask Applied to Image\nCell Count: {cell_count}')
    
        # fig.add_subplot(rows, cols, 5)
        # # display original image
        # plt.imshow(binary_mask2, cmap="gray")
        # plt.axis('on')
        # plt.title('Yen Thresholding Method Bitmask')
    
        # fig.add_subplot(rows, cols, 6)
        # # display original image
        # plt.imshow(summary_image2)
        # plt.axis('on')
        # plt.title(f'Yen Bitmask Applied to Image\nCell Count: {cell_count2}')
        # plt.savefig('../../Desktop/test.png')
    
        # cv2.imwrite("../../Desktop/greenImgs/spec_1/frame_1/results/Otsu"+str(img_number)+".png", summary_image)
        # img_number +=1     
    
    
