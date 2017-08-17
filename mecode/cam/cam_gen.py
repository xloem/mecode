import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

class camGen(object):
    def __init__(self,scan_file_location,start_x,start_y,pitch_x,pitch_y):
        self.f = np.load(scan_file_location)
        self.start_x = start_x
        self.start_y = start_y
        self.pitch_x = pitch_x
        self.pitch_y = pitch_y
        self.axis_names = ['a','b','c','d','XX','YY','ZZ','UU','AA2','BB2','CC2','DD','xxl','yyl','zzl','uul']

    def run(self,x_pos,y_pos):
        #Create plot to show cam pathes
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        #y_len = len(self.f)*self.pitch_y
        y_len = 1000*0.3
        #num_points = len(self.f)-19
        num_points = 982
        preamble = """Number of Points\t{} 
Master Units\t(PRIMARY) 
Slave Units\t(PRIMARY)
""".format(num_points)
        f = dict.fromkeys(self.axis_names)
        offset = 375.620-366.35
        nozzle_spacing = 2.5
        plot_vals = []
        for index,axis in enumerate(self.axis_names):
            f[axis] = open('{}_sine.cam'.format(axis),'w')
            f[axis].write(preamble)
            count = 1
            axis_plot_vals = []
            for y_val in np.arange(y_pos,0.3+y_len,self.pitch_y):
                x_val = x_pos+index*nozzle_spacing
                z_val = self.retrieve(x_val,y_val)
                f[axis].write('{:04d}\t{:06f}\t{:06f}\n'.format(count,y_val+offset,z_val))
                axis_plot_vals.append([x_val,y_val,z_val])
                count += 1
            plot_vals.append(axis_plot_vals)
        f[axis].close()
        #np.save('plot_vals.npy',np.array(plot_vals))
        for index,nozzle in enumerate(np.array(plot_vals)):
            x_vals = nozzle[:,0]
            y_vals = nozzle[:,1]
            z_vals = nozzle[:,2]
            ax.plot(x_vals,y_vals,z_vals,label= self.axis_names[index])

        plt.legend()
        plt.title('Generated Camming Profiles')
        plt.show()

    def retrieve(self,x,y):
        x_index = (x-self.start_x)/self.pitch_x
        y_index = (y-self.start_y)/self.pitch_y

        if x_index.is_integer() and y_index.is_integer():
            #print "Mode 1"
            return self.f[int(y_index),int(x_index)]

        elif x_index.is_integer() and not y_index.is_integer():
            #print "Mode 2"
            y_min = np.floor(y_index)
            y_max = np.ceil(y_index)
            return (y_max-y_index)/1*self.f[int(y_min),int(x_index)]+(y_index-y_min)/1*self.f[int(y_max),int(x_index)]

        elif y_index.is_integer() and not x_index.is_integer():
            #print "Mode 3"
            x_min = np.floor(x_index)
            x_max = np.ceil(x_index)
            return (x_max-x_index)/1*self.f[int(y_index),int(x_min)]+(x_index-x_min)/1*self.f[int(y_index),int(x_max)]
        
        else:
            #print "Mode 4"
            x_min = np.floor(x_index)
            x_max = np.ceil(x_index)
            y_min = np.floor(y_index)
            y_max = np.ceil(y_index)
            points = [(x_min,y_min,self.f[int(y_min),int(x_min)]),
                     (x_min,y_max,self.f[int(y_max),int(x_min)]),
                     (x_max,y_min,self.f[int(y_min),int(x_max)]),
                     (x_max,y_max,self.f[int(y_max),int(x_max)])]
            return self.bilinear_interpolation(x_index,y_index,points)

    def bilinear_interpolation(self,x, y, points):
        '''Interpolate (x,y) from values associated with four points.

        The four points are a list of four triplets:  (x, y, value).
        The four points can be in any order.  They should form a rectangle.

            >>> bilinear_interpolation(12, 5.5,
            ...                        [(10, 4, 100),
            ...                         (20, 4, 200),
            ...                         (10, 6, 150),
            ...                         (20, 6, 300)])
            165.0

        '''
        # See formula at:  http://en.wikipedia.org/wiki/Bilinear_interpolation
        points = sorted(points)               # order points by x, then by y

        try:
            (x1, y1, q11), (_x1, y2, q12), (x2, _y1, q21), (_x2, _y2, q22) = points
        except:
            print points

        if x1 != _x1 or x2 != _x2 or y1 != _y1 or y2 != _y2:
            print points
            print 'x: {}, y: {}'.format(x,y)
            raise ValueError('points do not form a rectangle')


        if not x1 <= x <= x2 or not y1 <= y <= y2:
            print points
            print 'x: {}, y: {}'.format(x,y)
            raise ValueError('(x, y) not within the rectangle')


        return (q11 * (x2 - x) * (y2 - y) +
                q21 * (x - x1) * (y2 - y) +
                q12 * (x2 - x) * (y - y1) +
                q22 * (x - x1) * (y - y1)
               ) / ((x2 - x1) * (y2 - y1) + 0.0)