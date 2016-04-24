import cv2
import numpy as np
# from matplotlib import pyplot as plt

def watershed(path):
	image = cv2.imread(path)
	gray_image = cv2.cvtColor(image, cv2.cv.CV_BGR2GRAY)
	ret,thresh = cv2.threshold(gray_image,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
	foreground = cv2.erode(thresh, None, iterations = 1)
	background = cv2.dilate(thresh, None, iterations = 1)
	ret,background = cv2.threshold(background,1,128,1)
	marker = cv2.add(foreground,background)
	canny = cv2.Canny(marker,110,150)
	contoured_image, contours, hierarchy = cv2.findContours(canny, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	#plt.imshow(contoured_image)
	#plt.show()
	marker32 = np.int32(marker)
	cv2.watershed(image,marker32)
	m = cv2.convertScaleAbs(marker32)
	ret,thresh = cv2.threshold(m,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
	thresh_not = cv2.bitwise_not(thresh)
	res = cv2.bitwise_and(image,image,mask = thresh)
	res2 = cv2.bitwise_and(image,image,mask=thresh_not)
	res3 = cv2.addWeighted(res,1,res2,1,0)
	final = cv2.drawContours(res3, contours, -1, (255, 0, 0), 1)

	return final
	#plt.imshow(res)
	#plt.show()

#watershed('baboon.jpg')
