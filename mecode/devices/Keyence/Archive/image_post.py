import numpy as np
from PIL import Image,ImageDraw
scan = np.load('calibration_fixture.npy')
polygon = list(np.load('side3.npy').flatten().astype(int))
#polygon = [390,558,430,595,444,594,478,560]
img = Image.new('1',(800,800),0)
ImageDraw.Draw(img).polygon(polygon,outline=1,fill=1)
mask = np.array(img)

for i in range(800):	
	for j in range(800):
		if mask[i,j] == False:
			scan[i,j] = np.nan
img.show()
np.save('isolated_scan3.npy',scan)