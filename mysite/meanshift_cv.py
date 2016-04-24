import cv2
# import numpy as np
# from matplotlib import pyplot as plt


def meanshift_cv(path):
	image = cv2.imread(path)
	spatial_window = 14
	color_window = 51
	shifted = cv2.pyrMeanShiftFiltering(image, spatial_window, color_window)
	return shifted
	# plt.imshow(shifted)
	# plt.show()

# meanshift_cv('baboon.jpg')

