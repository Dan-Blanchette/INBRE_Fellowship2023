import ipympl
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

path = os.getenv('HOME', default=0)


im_path = os.path.join(path + '/Desktop/greenImgs/spec_1/frame_1/013020_Lgalsbpb_GFPpos_NoTreatment_T01_XY1_Z10_RGB_Green.tif')

image = io.imread(im_path, plugin='pil')

plt.imshow(image)
plt.show()