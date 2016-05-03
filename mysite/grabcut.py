import cv2
import numpy as np
# from matplotlib import pyplot as plt

def grab_cut(path, x, y, width, height):
	image = cv2.imread(path)
	#h,w,c=image.shape
	#print h,w

	mask = np.zeros(image.shape[:2], np.uint8)
	background = np.zeros((1, 65), np.float64)
	foreground = np.zeros((1, 65), np.float64)
	rectangle = (int(x), int(y), int(width), int(height))

	#image - input image
	#mask - mask image of same size as image, initialized with zeros
	#rectangle - upper left coordinates of foreground object with format (x,y,width,height)
	#background - temp matrix used by algorithm
	#foreground - temp matrix used by algorithm
	#number of iterations
	#mode - run with mask or with rectangle
	num_iter = 1
	cv2.grabCut(image,mask, rectangle, background, foreground, num_iter, cv2.GC_INIT_WITH_RECT)

	mask2 = np.where((mask==2)|(mask==0),0,1).astype('uint8')
	image=image*mask2[:,:,np.newaxis]
	return image
	# plt.imshow(image)
	# plt.show()


# rect = (0,100,480,320)

# grab_cut('input1.jpg', rect)
