import cv2
import numpy as np
from matplotlib import pyplot as plt

def watershed(path):
	image = cv2.imread(path)
	gray_image = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
	ret,thresh = cv2.threshold(gray_image,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
	foreground = cv2.erode(thresh, None, iterations = 3)
	background = cv2.dilate(thresh, None, iterations = 3)
	ret,background = cv2.threshold(background,1,128,1)
	marker = cv2.add(foreground,background)

	marker32 = np.int32(marker)
	cv2.watershed(image,marker32)
	m = cv2.convertScaleAbs(marker32)
	ret,thresh = cv2.threshold(m,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
	res = cv2.bitwise_and(image,image,mask = thresh)
	plt.imshow(res)
	plt.show()
	
watershed('baboon.jpg')
