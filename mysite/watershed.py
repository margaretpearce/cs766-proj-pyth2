import cv2
import numpy as np
import random
#from matplotlib import pyplot as plt

def color_in_use(color, colors_used):
	for c in colors_used:
		if color == c:
			return True
	return False

def watershed(path):
	image = cv2.imread(path)
	gray_image = cv2.cvtColor(image, cv2.cv.CV_BGR2GRAY)
	gray_blur = cv2.GaussianBlur(gray_image, (5,5), 0)
	#ret,thresh = cv2.threshold(gray_image,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
	thresh = cv2.adaptiveThreshold(gray_blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,11,2)
	kernel = np.ones((1,1), np.uint8)
	opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=2)
	closing = cv2.dilate(opening,kernel,iterations=2)
	contours, hierarchy = cv2.findContours(closing, cv2.cv.CV_RETR_TREE,cv2.cv.CV_CHAIN_APPROX_SIMPLE)
	markers = np.zeros((gray_blur.shape[0], gray_blur.shape[1]),dtype = np.int32)
	markers = np.int32(closing) + np.int32(opening)
	markers = markers + 1
	cv2.watershed(image,markers)
	colors_used=[]

	for mark in np.unique(markers):
		if mark == 1:
			continue
		r = lambda: random.randint(0, 255)
		color = [r(), r(), r()]
		while(color_in_use(color,colors_used)):
			color = [r(),r(),r()]
		colors_used.append(color)
		image[mark == markers] = color

	return image
	#foreground = cv2.erode(thresh, None, iterations = 1)
	#background = cv2.dilate(thresh, None, iterations = 1)
	#ret,background = cv2.threshold(background,1,128,1)
	#marker = cv2.add(foreground,background)
	#canny = cv2.Canny(marker,110,150)
	#contoured_image, contours, hierarchy = cv2.findContours(canny, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	#plt.imshow(contoured_image)
	#plt.show()
	#marker32 = np.int32(marker)
	#cv2.watershed(image,marker32)
	#m = cv2.convertScaleAbs(marker32)
	#ret,thresh = cv2.threshold(m,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
	#thresh_not = cv2.bitwise_not(thresh)
	#res = cv2.bitwise_and(image,image,mask = thresh)
	#res2 = cv2.bitwise_and(image,image,mask=thresh_not)
	#res3 = cv2.addWeighted(res,1,res2,1,0)
	#final = cv2.drawContours(res3, contours, -1, (255, 0, 0), 1)


#watershed('/home/imagesegmentation/mysite/static/baboon.jpg')
