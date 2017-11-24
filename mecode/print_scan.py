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
g = G(scanner=True,direct_write=True,print_lines=False)
g.rename_axis(z='A')

#Create log file
log = open('print_log.txt','w')

#Experiment parameters
press_interval = {'min':20, 'max':35, 'step':2} #PSI
feed_interval = {'min':5, 'max':10, 'step':2} #mm/s
height_interval = {'min':0.3, 'max':0.5, 'step':0.05} #mm
start_delay = {'min':0.4, 'max':0.4, 'step':0.1}
iterations = 1
random_order = True

#Printer settings
efd_com_port = 3
rows = 30
travel_feed = 30 #mm/s
scanning_feed = 5 #mm/s
inital_dwell = 0.5 #s
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
start = np.arange(start_delay['min'],start_delay['max']+start_delay['step']-0.01,start_delay['step'])

test_cases = list(itertools.product(pressure,feedrate,height,start))
num_exp = len(test_cases)

#Randomize list (Could be useful?) Could randomize before of after iteration
if random_order:
	random.shuffle(test_cases)

#Add iterations
if iterations > 1:
	test_cases = [val for val in test_cases for _ in range(iterations)]

#Function to print individual line
def printLine(pressure,feedrate,height,start):
	g.set_pressure(3,pressure)
	g.abs_move(z=height)
	g.feed(feedrate)
	g.toggle_pressure(3)
	g.dwell(start)
	g.move(x=line_length)
	g.toggle_pressure(3)
	g.feed(travel_feed)
	g.move(x=end_wipe)
	g.abs_move(z=travel_height)
	g.move(x=-end_wipe)

#Function to initialize a scan of the printed line
def scanLine():
	g.move(x=scanner_buffer-scanner_offset['x'])
	
	#Start recording
	g.feed(scanning_feed)
	data = g.scan_strip(-line_length-2*scanner_buffer)
	
	g.feed(travel_feed)
	return data

#Funciton for converting 2D arrays to .csv point clouds for viewing
def point_cloud(data,filename):
	file = open('scans/{}.csv'.format(filename),'w')
	IXPitch, IYPitch, IXStart, IYStart = 0.05,0.05,0,0

	for i in range(len(data)):
		for j in range(len(data[0])):
			if not np.isnan(data[i,j]):
				x = IXStart + j*IXPitch
				y = IYStart + i*IYPitch
				z = data[i,j]
				file.write('{},{},{}\n'.format(x,y,z))
	file.close()

#Display experiement info
print_info = "Number of lines: {}, Number of Rows: {}, Number of Columns: {}".format(num_exp,rows,int(np.floor(num_exp/rows)))
log = open('print_log.txt','a')
log.write(print_info+"\n")
log.close()
print print_info

#Estimate print time
average_start_delay = (start_delay['min']+start_delay['max'])/2
average_feed = (feed_interval['min']+feed_interval['max'])/2
average_print_height = (height_interval['min']+height_interval['max'])/2
travel_distance = np.sqrt((scanner_buffer+scanner_offset['x'])**2 + del_y**2) + 2*(travel_height-average_print_height)
individual_line_print_time = average_start_delay + line_length/average_feed + travel_distance/travel_feed
scanning_time = np.abs(scanner_buffer-scanner_offset['x'])/travel_feed + np.abs(-line_length-2*scanner_buffer)/scanning_feed
switch_columns = del_x/travel_feed + (rows*del_y)/travel_feed
print_time = (individual_line_print_time + scanning_time)*num_exp + np.floor(num_exp/rows)*switch_columns
m, s = divmod(print_time, 60)
h, m = divmod(m, 60)
print "Time estimated to complete:	%d:%02d:%02d" % (h, m, s)

#Move to initial position defined by G92
g.feed(travel_feed)
g.abs_move(x=0,y=0)
data = np.array([])

i =0 
for test in test_cases:
	#Logging
	status = "Pressure: {}, Feedrate: {}, Height: {}, Start Delay: {}".format(*test)
	log = open('print_log.txt','a')
	log.write(status+"\n")
	log.close()
	print "Printing Line {} with:".format(i+1)
	print status
	
	#Printing
	printLine(*test)

	#Scanning
	scan_data = scanLine()
	filename_par = np.array(test)*10
	filename = '{}-P{}F{}H{}S{}'.format(i,*filename_par.astype(int))
	np.save('scans/{}-P{}F{}H{}S{}'.format(i,*filename_par.astype(int)),scan_data)
	point_cloud(scan_data,filename)
	np.append(data,scan_data)

	
	#Move to next position
	g.move(x=scanner_buffer+scanner_offset['x'],y=del_y)
	
	#Check if switching to next column
	i += 1
	if i % rows == 0:
		g.abs_move(y=0)
		g.move(x=del_x)

np.save('scan_data',scan_data)