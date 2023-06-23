from skimage import io
import os
import numpy as np
import glob
import matplotlib.pyplot as plt
import ipympl
import cv2
import re
# import imageio.v3 as iio
from skimage import color
from skimage import filters
from skimage import measure
from skimage import img_as_ubyte

image_list =[]

#select the path
path = "../../Desktop/greenImgs/spec_1/frame_1/*.tif"
img_number = 1  #Start an iterator for image number.
#This number can be later added to output image file names.


# sort  
for file in sorted(glob.glob(path)):
    print(file)     # see all file names printed
    img = io.imread(file, plugin='pil')  #now, we can read each file since we have the full path
    # plt.imshow(img)
    # plt.show()


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
    
    
