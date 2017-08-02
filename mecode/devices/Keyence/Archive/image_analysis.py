import numpy as np
import cv2
import matplotlib.pyplot as plt

img = cv2.imread('side2.png')
#gray = cv2.medianBlur(img,7)
#gray = cv2.GaussianBlur(img, (19, 19), 0)
gray = cv2.bilateralFilter(img,5,750,750)

edged = cv2.Canny(gray, 300, 500)

#cv2.imshow('gray',gray)
#cv2.imshow('edged',edged)

kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7))
closed = cv2.morphologyEx(edged, cv2.MORPH_CLOSE, kernel)
_, cnts, _ = cv2.findContours(closed.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

largeArea = 0
# loop over the contours
for c in cnts:
	# approximate the contour
	peri = cv2.arcLength(c, True)
	approx = cv2.approxPolyDP(c, 0.03 * peri, True)

	if len(approx) == 4:
		if cv2.contourArea(approx) > largeArea:
			largestContour = approx
			largeArea = cv2.contourArea(approx)


cv2.drawContours(img, [largestContour], -1, (0, 255, 0), 1)
print(largestContour)
#np.save('side3.npy',largestContour)
cv2.imshow('img',img)

cv2.waitKey(0)
cv2.destroyAllWindows()
