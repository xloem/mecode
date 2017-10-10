"""
Script for generation of raw direct-write data
==============================================

Should be able to simply define limits and step size for each printing property.
The three properties currently being investigated are:

1. Pressure
2. Feedrate
3. Height

Script should be able to discretize the parameters into a number of printed lines
to conduct the experiment, lay it out and print/scan the results. For now, simply 
saving the raw data will suffice. Could look at elminating extermes from test cases.
For instance, trimming the parameter space from a cube to a sphere.

"""
__author__ = "Robert Weeks"
__email__ = "rweeks@g.harvard.edu"
__version__ = "1.0"

from main import G
import numpy as np
import itertools
import random

#Initial printer setup
g = G(scanner=False,direct_write=True,print_lines=False)
g.rename_axis(z='A')

#Experiment parameters
press_interval = {'min':4, 'max':5, 'step':0.2} #PSI
feed_interval = {'min':4, 'max':8, 'step':1} #mm/s
height_interval = {'min':0.3, 'max':0.5, 'step':0.05} #mm
iterations = 1
random_order = True

#Printer settings
efd_com_port = 3
rows = 15
travel_feed = 20 #mm/s
inital_dwell = 0.5 #s
travel_height = 5 #mm
line_length = 15 #mm
del_y = 3 #mm
del_x = 30 #mm
scanner_offset = {'x':203, 'y':120} #mm

#Generate parameter space
pressure = np.arange(press_interval['min'],press_interval['max']+press_interval['step']-0.01,press_interval['step'])
feedrate = np.arange(feed_interval['min'],feed_interval['max']+feed_interval['step']-0.01,feed_interval['step'])
height = np.arange(height_interval['min'],height_interval['max']+height_interval['step']-0.01,height_interval['step'])

test_cases = list(itertools.product(pressure,feedrate,height))
num_exp = len(pressure)*len(feedrate)*len(height)*iterations

#Randomize list (Could be useful?) Could randomize before of after iteration
if random_order:
	random.shuffle(test_cases)

#Add iterations
if iterations > 1:
	test_cases = [val for val in test_cases for _ in range(iterations)]

#Function to print individual line
def printLine(pressure,feedrate,height):
	g.set_pressure(3,pressure)
	g.abs_move(z=height)
	g.feed(feedrate)
	g.toggle_pressure(3)
	g.dwell(0.5)
	g.move(x=line_length)
	g.toggle_pressure(3)
	g.feed(travel_feed)
	g.abs_move(z=travel_height)

#Move to initial position defined by G92
g.abs_move(x=0,y=0)

i =0 
for test in test_cases:
	print "Pressure: {}, Feedrate: {}, Height: {}".format(*test)
	printLine(*test)
	i += 1
	g.move(x=-line_length,y=del_y)
	if i % rows == 0:
		g.abs_move(y=0)
		g.move(x=del_x)