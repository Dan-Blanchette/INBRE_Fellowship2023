import matplotlib.pyplot as plt
import numpy as np
from skimage import io
import os

current_dir = os.getcwd()
print(current_dir)

path = str(current_dir) + "/frames_1/013020_Lgalsbpb_GFPpos_NoTreatment_T01_XY1_Z01_RGB_Green.tif"

print(path)
im = io.imread(path, plugin='pil')

imarray = np.array(im)

# print(imarray.shape)
# print(imarray.size)
# print(imarray)
plt.imshow(im)




# import glob, os

# path = str(os.getcwd() + "/frames_1/")

# print(path)

# list = []

# # dirs=directories
# for (root, dirs, files) in os.walk(path):
#     for f in files:
#         if '.tif' in f:
#             print(f)