import cv2

def thresholding(path):
    if path is not None:
        # Read in the image
        image = cv2.imread(path)

        # Convert to grayscale
        gray_img = cv2.cvtColor(image, cv2.cv.CV_BGR2GRAY)

        # Gaussian smoothing on the grayscale image
        gaussian_blur = cv2.GaussianBlur(gray_img, (5,5), 0)

        # Thresholding
        ret, thres_img = cv2.threshold(gaussian_blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        # Return the new image
        return (thres_img, ret)
    else:
        return None