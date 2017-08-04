import numpy as np
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import cv2

scan = np.load('calibration_fixture.npy')
gradX, gradY = np.nan_to_num(np.gradient(scan)) #[0]:X [1]:Y
sides = [np.copy(gradX),np.copy(gradX),np.copy(gradY),np.copy(gradY)]

def fit_to_plane(points):
	xs = points[:,0]
	ys = points[:,1]
	zs = points[:,2]

	# do fit
	tmp_A = []
	tmp_b = []
	for i in range(len(xs)):
	    tmp_A.append([xs[i], ys[i], 1])
	    tmp_b.append(zs[i])
	b = np.matrix(tmp_b).T
	A = np.matrix(tmp_A)
	fit = (A.T * A).I * A.T * b
	errors = b - A * fit
	residual = np.linalg.norm(errors)

	"""
	print("solution:")
	print("%f x + %f y + %f = z" % (fit[0], fit[1], fit[2]))
	#print "errors:"
	#print errors
	print("residual:")
	print(residual)
	"""
	return [float(fit[0]),float(fit[1]),float(-1),float(fit[2])]

def intersection_of_planes(planes):
	#Using Cramer's rule
	p1 = planes[0]
	p2 = planes[1]
	p3 = planes[2]
	x_t = np.array([[p1[3],p1[1],p1[2]],
				    [p2[3],p2[1],p2[2]],
				    [p3[3],p3[1],p3[2]]])
	y_t = np.array([[p1[0],p1[3],p1[2]],
				    [p2[0],p2[3],p2[2]],
				    [p3[0],p3[3],p3[2]]])
	z_t = np.array([[p1[0],p1[1],p1[3]],
				    [p2[0],p2[1],p2[3]],
				    [p3[0],p3[1],p3[3]]])
	det = np.array([[p1[0],p1[1],p1[2]],
				    [p2[0],p2[1],p2[2]],
				    [p3[0],p3[1],p3[2]]])
	det = np.linalg.det(det)
	
	x = np.linalg.det(x_t)/det
	y = np.linalg.det(y_t)/det
	z = np.linalg.det(z_t)/det
	return [-x,-y,-z]
	
	return "Complete"

planes = []
for index, side in enumerate(sides):
	for x in np.nditer(side,op_flags=['readwrite']):
		if index%2 == 0:
			if x < -0.6 or x > -0.2:
				x[...] = 0
		else:
			if x > 0.6 or x < 0.2:
				x[...] = 0
	if index%2 == 0:
		side = side/np.amin(side)
	else:
		side = side/np.amax(side)
	#side = Image.fromarray(np.uint8(side*255))
	#side.save('side{}.png'.format(index+1))
	#side = cv2.imread('side{}.png'.format(index+1))
	
	side = np.uint8(side*255)
	
	if index in [1,2,3]:
		gray = cv2.bilateralFilter(side,5,750,750)
		edged = cv2.Canny(gray, 250, 500)
		#cv2.imshow('gray{}'.format(index+1),gray)
		#cv2.imshow('edged{}'.format(index+1),edged)
		kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7))
		closed = cv2.morphologyEx(edged, cv2.MORPH_CLOSE, kernel)
		_, cnts, _ = cv2.findContours(closed.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

		largeArea = 0
		# loop over the contours
		for c in cnts:
			# approximate the contour
			peri = cv2.arcLength(c, True)
			approx = cv2.approxPolyDP(c, 0.03 * peri, True)
			#cv2.drawContours(side, [approx], -1, (255), 2)

			if len(approx) == 4:
				if cv2.contourArea(approx) > largeArea:
					largestContour = approx
					largeArea = cv2.contourArea(approx)
		cv2.drawContours(side, [largestContour], -1, (255), 3)
		#print(largestContour)
		#cv2.imshow('img{}'.format(index+1),side)

		polygon = list(largestContour.flatten().astype(int))
		img = Image.new('1',(len(scan),len(scan[0])),0)
		ImageDraw.Draw(img).polygon(polygon,outline=1,fill=1)
		mask = np.array(img)
		#img.show()

		IXStart = -120.0
		IXPitch = 0.3
		IYStart = 0
		IYPitch = 0.3
		points = []
		for i in range(len(scan)):	
			for j in range(len(scan[0])):
				if mask[i,j]:
					x = IXStart + j*IXPitch
					y = IYStart + i*IYPitch
					z = scan[i,j]
					points.append([x,y,z])
		planes.append(fit_to_plane(np.array(points)))

print("The location of the pyramid is:")
print("x:{:.2f} y:{:.2f} z:{:.2f}".format(*intersection_of_planes(planes)))
#cv2.waitKey(0)
#cv2.destroyAllWindows()


