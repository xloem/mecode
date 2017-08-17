import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
x_pos = np.array([300]*401)
z_travel = -12
y_travel = 400
num_points = 401
a = open('a_sine.cam','w') 
b = open('b_sine.cam','w') 
c = open('c_sine.cam','w') 
d = open('d_sine.cam','w')
XX = open('XX_sine.cam','w') 
YY = open('YY_sine.cam','w') 
ZZ = open('ZZ_sine.cam','w') 
UU = open('UU_sine.cam','w')
AA2 = open('AA2_sine.cam','w') 
BB2 = open('BB2_sine.cam','w') 
CC2 = open('CC2_sine.cam','w') 
DD = open('DD_sine.cam','w')
xxl = open('xxl_sine.cam','w') 
yyl = open('yyl_sine.cam','w') 
zzl = open('zzl_sine.cam','w') 
uul = open('uul_sine.cam','w')   

preamble = """Number of Points\t{} 
Master Units\t(PRIMARY) 
Slave Units\t(PRIMARY)
""".format(num_points)

a.write(preamble)
b.write(preamble)
c.write(preamble)
d.write(preamble)
XX.write(preamble)
YY.write(preamble)
ZZ.write(preamble)
UU.write(preamble)
AA2.write(preamble)
BB2.write(preamble)
CC2.write(preamble)
DD.write(preamble)
xxl.write(preamble)
yyl.write(preamble)
zzl.write(preamble)
uul.write(preamble)

count = 1
for y_pos in np.linspace(0,400,401):
	a_pos = -z_travel/2*np.sin(np.pi/(y_travel/4)*y_pos)-z_travel/2
	b_pos = -z_travel/2*np.sin(np.pi/(y_travel/4)*(y_pos+10))-z_travel/2
	c_pos = -z_travel/2*np.sin(np.pi/(y_travel/4)*(y_pos+20))-z_travel/2
	d_pos = -z_travel/2*np.sin(np.pi/(y_travel/4)*(y_pos+30))-z_travel/2
	XX_pos = -z_travel/2*np.sin(np.pi/(y_travel/4)*(y_pos+40))-z_travel/2
	YY_pos = -z_travel/2*np.sin(np.pi/(y_travel/4)*(y_pos+50))-z_travel/2
	ZZ_pos = -z_travel/2*np.sin(np.pi/(y_travel/4)*(y_pos+60))-z_travel/2
	UU_pos = -z_travel/2*np.sin(np.pi/(y_travel/4)*(y_pos+70))-z_travel/2
	AA2_pos = -z_travel/2*np.sin(np.pi/(y_travel/4)*(y_pos+80))-z_travel/2
	BB2_pos = -z_travel/2*np.sin(np.pi/(y_travel/4)*(y_pos+90))-z_travel/2
	CC2_pos = -z_travel/2*np.sin(np.pi/(y_travel/4)*(y_pos+100))-z_travel/2
	DD_pos = -z_travel/2*np.sin(np.pi/(y_travel/4)*(y_pos+110))-z_travel/2
	xxl_pos = -z_travel/2*np.sin(np.pi/(y_travel/4)*(y_pos+120))-z_travel/2
	yyl_pos = -z_travel/2*np.sin(np.pi/(y_travel/4)*(y_pos+130))-z_travel/2
	zzl_pos = -z_travel/2*np.sin(np.pi/(y_travel/4)*(y_pos+140))-z_travel/2
	uul_pos = -z_travel/2*np.sin(np.pi/(y_travel/4)*(y_pos+150))-z_travel/2
	a.write('{:04d}\t{:06f}\t{:06f}\n'.format(count,y_pos,a_pos))
	b.write('{:04d}\t{:06f}\t{:06f}\n'.format(count,y_pos,b_pos))
	c.write('{:04d}\t{:06f}\t{:06f}\n'.format(count,y_pos,c_pos))
	d.write('{:04d}\t{:06f}\t{:06f}\n'.format(count,y_pos,d_pos))
	XX.write('{:04d}\t{:06f}\t{:06f}\n'.format(count,y_pos,XX_pos))
	YY.write('{:04d}\t{:06f}\t{:06f}\n'.format(count,y_pos,YY_pos))
	ZZ.write('{:04d}\t{:06f}\t{:06f}\n'.format(count,y_pos,ZZ_pos))
	UU.write('{:04d}\t{:06f}\t{:06f}\n'.format(count,y_pos,UU_pos))
	AA2.write('{:04d}\t{:06f}\t{:06f}\n'.format(count,y_pos,AA2_pos))
	BB2.write('{:04d}\t{:06f}\t{:06f}\n'.format(count,y_pos,BB2_pos))
	CC2.write('{:04d}\t{:06f}\t{:06f}\n'.format(count,y_pos,CC2_pos))
	DD.write('{:04d}\t{:06f}\t{:06f}\n'.format(count,y_pos,DD_pos))
	xxl.write('{:04d}\t{:06f}\t{:06f}\n'.format(count,y_pos,xxl_pos))
	yyl.write('{:04d}\t{:06f}\t{:06f}\n'.format(count,y_pos,yyl_pos))
	zzl.write('{:04d}\t{:06f}\t{:06f}\n'.format(count,y_pos,zzl_pos))
	uul.write('{:04d}\t{:06f}\t{:06f}\n'.format(count,y_pos,uul_pos))
	if count ==1:
		print "a_pos = {}".format(a_pos)
		print "b_pos = {}".format(b_pos)
		print "c_pos = {}".format(c_pos)
		print "d_pos = {}".format(d_pos)
		print "XX_pos = {}".format(XX_pos)
		print "YY_pos = {}".format(YY_pos)
		print "ZZ_pos = {}".format(ZZ_pos)
		print "UU_pos = {}".format(UU_pos)
		print "AA2_pos = {}".format(AA2_pos)
		print "BB2_pos = {}".format(BB2_pos)
		print "CC2_pos = {}".format(CC2_pos)
		print "DD_pos = {}".format(DD_pos)
		print "xx_pos = {}".format(xxl_pos)
		print "yy_pos = {}".format(yyl_pos)
		print "zz_pos = {}".format(zzl_pos)
		print "uu_pos = {}".format(uul_pos)

	count += 1

a.close()
b.close()
c.close()
d.close()
XX.close()
YY.close()
ZZ.close()
UU.close()
AA2.close()
BB2.close()
CC2.close()
DD.close()
xxl.close()
yyl.close()
zzl.close()
uul.close()

#Show proposed toolpathes
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
y_pos = np.linspace(0,400,401)
a_pos = -z_travel/2*np.sin(np.pi/(y_travel/4)*y_pos)-z_travel/2
b_pos = -z_travel/2*np.sin(np.pi/(y_travel/4)*(y_pos+10))-z_travel/2
c_pos = -z_travel/2*np.sin(np.pi/(y_travel/4)*(y_pos+20))-z_travel/2
d_pos = -z_travel/2*np.sin(np.pi/(y_travel/4)*(y_pos+30))-z_travel/2
XX_pos = -z_travel/2*np.sin(np.pi/(y_travel/4)*(y_pos+40))-z_travel/2
YY_pos = -z_travel/2*np.sin(np.pi/(y_travel/4)*(y_pos+50))-z_travel/2
ZZ_pos = -z_travel/2*np.sin(np.pi/(y_travel/4)*(y_pos+60))-z_travel/2
UU_pos = -z_travel/2*np.sin(np.pi/(y_travel/4)*(y_pos+70))-z_travel/2
AA2_pos = -z_travel/2*np.sin(np.pi/(y_travel/4)*(y_pos+80))-z_travel/2
BB2_pos = -z_travel/2*np.sin(np.pi/(y_travel/4)*(y_pos+90))-z_travel/2
CC2_pos = -z_travel/2*np.sin(np.pi/(y_travel/4)*(y_pos+100))-z_travel/2
DD_pos = -z_travel/2*np.sin(np.pi/(y_travel/4)*(y_pos+110))-z_travel/2
xxl_pos = -z_travel/2*np.sin(np.pi/(y_travel/4)*(y_pos+120))-z_travel/2
yyl_pos = -z_travel/2*np.sin(np.pi/(y_travel/4)*(y_pos+130))-z_travel/2
zzl_pos = -z_travel/2*np.sin(np.pi/(y_travel/4)*(y_pos+140))-z_travel/2
uul_pos = -z_travel/2*np.sin(np.pi/(y_travel/4)*(y_pos+150))-z_travel/2
ax.plot(x_pos+20,y_pos,a_pos,label= 'a')
ax.plot(x_pos+40,y_pos,b_pos,label= 'b')
ax.plot(x_pos+60,y_pos,c_pos,label= 'c')
ax.plot(x_pos+80,y_pos,d_pos,label= 'd')
ax.plot(x_pos+100,y_pos,XX_pos,label= 'XX')
ax.plot(x_pos+120,y_pos,YY_pos,label= 'YY')
ax.plot(x_pos+140,y_pos,ZZ_pos,label= 'ZZ')
ax.plot(x_pos+160,y_pos,UU_pos,label= 'UU')
ax.plot(x_pos+180,y_pos,AA2_pos,label= 'AA2')
ax.plot(x_pos+200,y_pos,BB2_pos,label= 'BB2')
ax.plot(x_pos+220,y_pos,CC2_pos,label= 'CC2')
ax.plot(x_pos+240,y_pos,DD_pos,label= 'DD')
ax.plot(x_pos+260,y_pos,xxl_pos,label= 'xx')
ax.plot(x_pos+280,y_pos,yyl_pos,label= 'yy')
ax.plot(x_pos+300,y_pos,zzl_pos,label= 'zz')
ax.plot(x_pos+320,y_pos,uul_pos,label= 'uu')
ax.set_xlabel('X (mm)')
ax.set_ylabel('Y (mm)')
ax.set_zlabel('Z (mm)')

plt.legend()
plt.title('Generated Sinusoidal Toolpaths')
plt.show()
