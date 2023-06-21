from PIL import Image
import skimage.io as io
import numpy as np

im = io.imread("../../Desktop/greenImgs/spec_1/frame_1/013020_Lgalsbpb_GFPpos_NoTreatment_T01_XY1_Z02_RGB_Green.tif")
# im.show()

# convert the image to a numpy array
imarray = np.array(im)

print(imarray.shape)

newArray = np.transpose(imarray, (2,0,1))
print(newArray.shape)

fixedImg = Image.fromarray(newArray)

