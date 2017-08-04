import numpy as np
from PIL import Image

scan = np.load('calibration_fixture.npy')
gradX, gradY = np.nan_to_num(np.gradient(scan)) #[0]:X [1]:Y
sides = [gradX,gradX,gradY,gradY]

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
	im_grad = Image.fromarray(np.uint8(side*255))
	im_grad.save('side{}.png'.format(index+1))