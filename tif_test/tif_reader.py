import matplotlib.pyplot as plt
from skimage import io

path = 'test1.tif'

im = io.imread(path, plugin='pil')
plt.imshow(im)