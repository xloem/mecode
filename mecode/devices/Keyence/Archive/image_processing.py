import numpy as np
from PIL import Image

scan = np.load('calibration_fixture.npy')
gradXY = np.nan_to_num(np.gradient(scan)) #[0]:X [1]:Y


for x in np.nditer(gradXY[1],op_flags=['readwrite']):
	if x < -0.5 or x > -0.45:
		x[...] = 0

gradXY[1] = gradXY[1]/np.amin(gradXY[1])
im_grad = Image.fromarray(np.uint8(gradXY[1]*255))
im_grad.save('side3.png')






