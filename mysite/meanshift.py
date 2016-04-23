from sklearn.cluster import MeanShift, estimate_bandwidth
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import cv2

def mean_shift(path):
	image = cv2.imread(path)
	image_reshape = image.reshape(image.shape[0]*image.shape[1],3)
	bw = estimate_bandwidth(image_reshape, quantile=0.2, n_samples=500)
	ms = MeanShift(21, bin_seeding=True)
	ms.fit(image_reshape)
	labels=ms.labels_
	cluster_centers = ms.cluster_centers_
	n_clus = len(np.unique(cluster_centers))
	#print n_clus
	quant = ms.cluster_centers_.astype("uint8")[labels]
	quant = quant.reshape((image.shape[0],image.shape[1],3))
	plt.imshow(quant)
	plt.show()
	
mean_shift('baboon.jpg')
