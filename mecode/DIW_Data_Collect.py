"""
Script for generation of raw direct-ink-write data
==============================================

Should be able to simply define limits and step size for each printing property.
The three properties currently being investigated are:

1. Pressure
2. Feedrate
3. Height

Script should be able to discretize the parameters into a number of printed lines
to conduct the experiment, lay it out and print/scan the results. For now, simply 
saving the raw data will suffice. Could look at elminating extermes from test cases.
For instance, trimming the parameter space from a cube to a sphere. Tweaking the order 
of test cases can be used to minimize messy print failures.

Saves the scans as numpy arrays in the format:
{count}-{pressure}-{feedrate}-{height}.npy

"""
__author__ = "Robert Weeks"
__email__ = "rweeks@g.harvard.edu"
__version__ = "1.0"

from main import G
import numpy as np
import itertools

#Initial printer setup
g = G(scanner=True,direct_write=True,print_lines=False)
g.rename_axis(z='A')

#Experiment parameters
press_interval = {'min':20, 'max':35, 'step':2} #PSI
feed_interval = {'min':5, 'max':10, 'step':2} #mm/s
height_interval = {'min':0.3, 'max':0.5, 'step':0.05} #mm

#Printer settings
efd_com_port = 3
rows = 30
travel_feed = 30 #mm/s
scanning_feed = 5 #mm/s
inital_dwell = 0.4 #s
travel_height = 3 #mm
line_length = 15 #mm
del_y = 3 #mm
del_x = 20 #mm
scanner_offset = {'x':34.366, 'y':0} #mm
scanner_buffer = 1.5 #mm
end_wipe = 5 #mm

#Generate parameter space
pressure = np.arange(press_interval['min'],press_interval['max']+press_interval['step']-0.01,press_interval['step'])
feedrate = np.arange(feed_interval['min'],feed_interval['max']+feed_interval['step']-0.01,feed_interval['step'])
height = np.arange(height_interval['min'],height_interval['max']+height_interval['step']-0.01,height_interval['step'])

#Generate individual test cases
test_cases = list(itertools.product(pressure,feedrate,height))

def printLine(pressure,feedrate,height):
	g.set_pressure(3,pressure)
	g.abs_move(z=height)
	g.feed(feedrate)
	g.toggle_pressure(3)
	g.dwell(inital_dwell)
	g.move(x=line_length)
	g.toggle_pressure(3)
	g.feed(travel_feed)
	g.move(x=end_wipe)
	g.abs_move(z=travel_height)
	g.move(x=-end_wipe)

def scanLine():
	g.move(x=scanner_buffer-scanner_offset['x'])
	g.feed(scanning_feed)
	data = g.scan_strip(-line_length-2*scanner_buffer)
	g.feed(travel_feed)
	return data

#Move to initial position defined by G92
g.feed(travel_feed)
g.abs_move(x=0,y=0)

#Loop though printing
for count, case in enumerate(test_cases):
	#Print line case
	printLine(*case)
	#Scan printed line
	scan_data = scanLine()
	np.save('{}-{:.1f}-{:.1f}-{:.2f}'.format(count,*case),scan_data)
	#Move to next position
	g.move(x=scanner_buffer+scanner_offset['x'],y=del_y)
	#Check if switching to next column is required
	if count % rows == 0:
		g.abs_move(y=0)
		g.move(x=del_x)