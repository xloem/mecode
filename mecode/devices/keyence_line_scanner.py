'''
Pipeline to communicate with Keyence Profilometer to python

Read measurements from Keyence Profilometer using the included dll
Must be used with python 2.7 32bit
Keyence Profilometer is simply plugged in over USB

Requires: os, numpy and ctypes
Only functions on windows due to dll
'''

__author__ = "Robert Weeks"
__email__ = "rweeks@seas.harvard.edu"
__version__ = 0.1

import os.path
from ctypes import *
import numpy as np

class KeyenceLineScanner(object):
	def __init__(self,device_id=0,model='7300',measurement_count=16):
		"""
		Parameters
		----------
		device_id : int (default: 0)
			Specifies device id of profilometer to connect to. Device ids start at 0.
		measurement_count : int (default : 16)
			Corresponds to the number of 'out' measurements programmed to the controller.
		model : String (default: '7300')
 			Specifies the sensor head model that is being used. This is used for scan path planning based on scaning width.
		"""
		if model == '7300':
			self.scan_width = 150.0
			self.IXPitch = 0.3
		elif model == '7080':
			self.scan_width = 30.0
			self.IXPitch = 0.05
		else:
			raise ValueError('Unknown model number.')

		self.device_id = device_id
		self.measurement_count = measurement_count
		#The number of data points along a line in the returned profile. Defaults to 800 for this line of scanners.
		self.max_profile_count = 800 

		#Dynamic Link Library Setup (assumes located in same directory)
		dll_name = "LJV7_IF.dll"
		dll_path = os.path.dirname(os.path.abspath(__file__)) + os.path.sep + dll_name
		self.scanner = windll.LoadLibrary(dll_path)
		self.connect()

	def setup_scan(self,start_pos,interval):
		"""
		Initialize the starting position in Y and pitch in Y
		"""
		self.IYStart = start_pos
		self.IYPitch = interval

	def connect(self):
		"""
		Initialize the dll and connect to the scanner over USB
		"""
		self.scanner.LJV7IF_Initialize()
		if self.scanner.LJV7IF_UsbOpen(self.device_id) != 0:
			raise IOError('Unable to connect to profilometer over USB')

	def disconnect(self):
		"""
		Disconnect the scanner and finalize the dll
		"""
		self.scanner.LJV7IF_CommClose(self.device_id)
		self.scanner.LJV7IF_Finalize()

	def reboot(self):
		"""
		This function reboots the controller and connected devices
		"""
		self.scanner.LJV7IF_RebootController(self.device_id)

	def trigger(self):
		"""
		Triggers the scanner to take a measurement
		"""
		return self.scanner.LJV7IF_Trigger(self.device_id)

	def clear_memory(self):
		"""
		Clears the memory of the scanner
		"""
		return self.scanner.LJV7IF_ClearMemory(self.device_id)

	def get_profile(self,profile_count,erase_after=False):
		"""
		Returns multiple profiles from memory using the high-speed mode

		Parameters
		----------
		profile_count = int
			Number of profiles to read from memory
		erase_after = bool (default: False)
			Whether or not to delete the values from memory after reading
		"""

		#Profile Request Setup
		req = self.LJV7IF_GET_PROFILE_REQ()
		req.byTargetBank = 0
		req.byPosMode = 0
		req.dwGetProfNo = 0
		req.byGetProfCnt = profile_count
		req.byErase = erase_after

		#Profile Response Setup
		rsp = self.LJV7IF_GET_PROFILE_RSP()

		#Profile Info Setup
		profileInfo = self.LJV7IF_PROFILE_INFO()

		#Profile Buffer Setup
		profileDataSize = self.max_profile_count + (sizeof(self.LJV7IF_PROFILE_HEADER) + sizeof(self.LJV7IF_PROFILE_FOOTER)) / sizeof(c_int);
		receiveBuffer = (c_int*(profileDataSize*req.byGetProfCnt))()
		dwDataSize = c_uint(profileDataSize*req.byGetProfCnt*sizeof(c_int))

		#Send request to scanner for profiles
		self.scanner.LJV7IF_GetProfile(self.device_id,byref(req),byref(rsp),byref(profileInfo),receiveBuffer,dwDataSize)

		#Process the received data
		profiles = np.frombuffer(receiveBuffer, np.intc).astype(float)
		
		#Replace error values with None
		for i, item in enumerate(profiles):
			if item in (-2147483648,-2147483647,-2147483646,-2147483645):
				profiles[i] = np.nan

		#profiles2d = np.reshape(profiles,(profile_count,-1))/100000.0
		profiles2d = profiles/100000.0
		#Save relevant profile info
		self.IXStart = profileInfo.IXStart/100000.0
		self.IXPitch = profileInfo.IXPitch/100000.0
		#self.byProfileCnt = profileInfo.byProfileCnt
		#self.wProfDataCnt = profileInfo.wProfDataCnt

		#Removes header and footer
		if profile_count > 1:
			profiles2d = np.reshape(profiles,(profile_count,-1))/100000.0
			return np.delete(profiles2d,range(6)+[len(profiles2d[0])-1],axis=1)
		else:
			profiles2d = profiles/100000.0
			return np.delete(profiles2d,range(6)+[len(profiles2d)-1])
	
	def get_measurement(self):
		"""
		Returns the 'out' data points as specified on the controller
		Note: Controller must be set to advanced mode
		"""
		#Measurement buffer setup
		rsp = (self.LJV7IF_MEASURE_DATA*self.measurement_count)()

		#Send request to scanner for measurements
		self.scanner.LJV7IF_GetMeasurementValue(self.device_id,rsp)
		return [rsp[i].fValue for i in range(self.measurement_count)]

	def stop_storage(self):
		self.scanner.LJV7IF_StopStorage(self.device_id)

	def start_storage(self):
		self.scanner.LJV7IF_StartStorage(self.device_id)

	def get_profile_storage(self,profile_count,erase_after=False):
		"""
		Returns multiple profiles from storage using the advanced mode
		Notes: Seems to only work for roughly <200 points? Don't know why.

		Parameters
		----------
		profile_count = int
			Number of profiles to read from storage
		erase_after = bool (default: False)
			Whether or not to delete the values from memory after reading
		"""

		#Profile Request Setup
		req = self.LJV7IF_GET_STORAGE_REQ()
		req.dwSurface = 1
		req.dwStartNo = 0
		req.dwDataCnt = profile_count

		#Profile Storage Response Setup
		rsp = self.LJV7IF_GET_STORAGE_RSP()

		#Profile Info Setup
		profileInfo = self.LJV7IF_PROFILE_INFO()

		#Storage Info Setup
		storageInfo = self.LJV7IF_STORAGE_INFO()

		#Profile Buffer Setup
		profileDataSize = self.max_profile_count + (sizeof(self.LJV7IF_PROFILE_HEADER) + sizeof(self.LJV7IF_PROFILE_FOOTER)) / sizeof(c_int);
		#receiveBuffer = ((c_uint + self.LJV7IF_MEASURE_DATA*16 + c_int*profileDataSize + self.LJV7IF_MEASURE_DATA*16)*req.dwDataCnt)()
		measureDataSize = sizeof(self.LJV7IF_MEASURE_DATA*16)/4
		receiveBuffer = (c_int*(profileDataSize+measureDataSize*2+1)*req.dwDataCnt*2)()
		dwDataSize = c_uint(((profileDataSize+measureDataSize*2+1)*req.dwDataCnt*2)*sizeof(c_int))

		#Send request to scanner for profiles
		self.scanner.LJV7IF_GetStorageProfile(self.device_id,byref(req),byref(storageInfo),byref(rsp),byref(profileInfo),receiveBuffer,dwDataSize)
		
		#Process the received data
		profiles = np.frombuffer(receiveBuffer, np.intc).astype(float)

		"""
		#Replace error values with None
		for i, item in enumerate(profiles):
			if item in (-2147483648,-2147483647,-2147483646,-2147483645):
				profiles[i] = np.nan

		profiles2d = np.reshape(profiles,(profile_count,-1))/100000.0

		#Save relevant profile info
		self.IXStart = profileInfo.IXStart/100000.0
		self.IXPitch = profileInfo.IXPitch/100000.0
		self.byProfileCnt = profileInfo.byProfileCnt
		self.wProfDataCnt = profileInfo.wProfDataCnt

		#Erase data from controller if requested
		if erase_after:
			self.clear_memory()

		#Removes header and footer
		return np.delete(profiles2d,range(39),axis=1)[:,:-33]
		"""
		return profiles

	def continuous_get_profiles(self,profile_count):
		"""
		Continuously read profiles from memory as they become available.
		Stops reading when it reads a specified number of counts.

		Parameters
		----------
		profile_count = int
			Number of profiles to read before stopping
		"""
		aquired = []
		aquiredCount = 0
		while aquiredCount < profile_count:
			if np.count_nonzero(self.get_profile(1)) != 0:
				aquired.append(self.get_profile(1,True))
				aquiredCount += 1
				print "Scanning...{0:.2f}%  \r".format(float(aquiredCount)/profile_count*100),
		print "\n"
		return np.array(aquired)

	def processScanResults(self,data,num_passes,scan_width,scan_trim):
		"""
		Cleans and correctly formats a 2d scan
		Parameters
		----------
		export_location = String
			Location to save exported .csv point cloud file
		data = float
			2D numpy array of scan data
		"""
		passes = np.vsplit(data,num_passes)
		passes_fixed = [np.fliplr(x) if ind%2 else np.fliplr(np.flipud(x)) for ind, x in enumerate(passes) ]
		passes_trimmed = [x[:,151:651] if ind>0 else x[:,150:651] for ind, x in enumerate(passes_fixed)]
		passes_final = np.hstack(passes_trimmed)
		trim_ind = int(scan_trim/self.IXPitch)
		passes_finalTrim = passes_final[:,trim_ind:-trim_ind]
		scan2d = np.flipud(passes_finalTrim)

		return scan2d

	def export_point_cloud(self,export_location,data):
		"""
		Exports a .csv file compatible with point cloud software for easy viewing

		Parameters
		----------
		export_location = String
			Location to save exported .csv point cloud file
		data = float
			2D numpy array of scan data
		"""

		file = open(export_location,'w')

		for i in range(len(data)):
			for j in range(len(data[0])):
				if not np.isnan(data[i,j]):
					x = self.IXStart + j*self.IXPitch
					y = self.IYStart + i*self.IYPitch
					z = data[i,j]
					file.write('{},{},{}\n'.format(x,y,z))
		file.close()


	class LJV7IF_MEASURE_DATA(Structure):
		"""
		Variable Definitions:

		byDataInfo
		----------
		The validity of a measurement value
		Valid = 0	Normal measurement data
		Alarm = 1	Decision standby data
		Wait = 2	Measurement alarm data

		byJudge
		-------
		Tolerance judgement result
		Hi = 1
		Go = 2
		Lo = 4

		fValue
		------
		Measurement value
		"""
		_fields_ = [
			("byDataInfo", c_ubyte),
			("byJudge", c_ubyte), 
			("reserve", c_ubyte * 2),
			("fValue", c_float)]

	class LJV7IF_GET_PROFILE_REQ(Structure):
		"""
		Parameter Definitions:

		byTargetBank
		----------
		Get profile target buffer specification
		Active = 0x00	Active surface
		Inactive = 0x01	Inactive surface

		byPosMode
		-------
		Get profile position specification method designation
		Current = 0x00	From current
		Oldest = 0x01	From oldest
		Spec = 0x02		Specify position

		dwGetProfNo
		-----------
		Get target profile number

		byGetProfCnt
		------------
		The number of profiles to read

		byErase
		-------
		Delete profiles read from the controller

		"""
		_fields_ = [
			("byTargetBank", c_ubyte),
			("byPosMode", c_ubyte), 
			("reserve", c_ubyte * 2),
			("dwGetProfNo", c_uint),
			("byGetProfCnt", c_ubyte),
			("byErase", c_ubyte), 
			("reserve2", c_ubyte * 2)]

	class LJV7IF_GET_PROFILE_RSP(Structure):
		"""
		Parameter Definitions:

		dwCurrentProfNo
		----------
		Current profile number

		dwOldestProfNo
		--------------
		Oldest profile number in the controller

		dwGetTopProNo
		-------------
		Starting number of the profiles that were read

		byGetTopProfNo
		--------------
		Number of profiles that were read
		"""
		_fields_ = [
			("dwCurrentProfNo", c_uint),
			("dwOldestProfNo", c_uint), 
			("dwGetTopProfNo", c_uint),
			("byGetProfCnt", c_ubyte), 
			("reserve", c_ubyte * 3)]

	class LJV7IF_PROFILE_INFO(Structure):
		"""
		Parameter Definitions:

		byProfileCnt
		------------
		Number of stored profile data

		byEnvelope
		----------
		Profile compression (time axis)

		wProfDataCnt
		------------
		Profile data amount

		IXStart
		-------
		X coordinate for the 1st point

		IXPitch
		-------
		Profile data X direction interval
		"""
		_fields_ = [
			("byProfileCnt", c_ubyte),
			("byEnvelope", c_ubyte), 
			("reserve", c_ubyte * 2),
			("wProfDataCnt", c_ushort),
			("reserve2", c_ubyte * 2),
			("IXStart", c_int), 
			("IXPitch", c_int)]

	class LJV7IF_PROFILE_HEADER(Structure):
		"""
		Parameter Definitions:

		dwTriggerCnt
		------------
		Number of triggers from the start of the measurements

		dwEncoderCnt
		------------
		Number of encoder triggers from the start of the measurements
		"""
		_fields_ = [
			("reserve", c_uint),
			("dwTriggerCnt", c_uint), 
			("dwEncoderCnt", c_uint),
			("reserve2", c_uint * 3)]

	class LJV7IF_PROFILE_FOOTER(Structure):
		_fields_ = [
			("reserve", c_uint)]

	class LJV7IF_GET_STORAGE_REQ(Structure):
		"""
		Parameter Definitions:

		dwSurface
		---------
		The storage surface to read
		When the memory allocation setting is "double buffer"
			0: Active surface, 1:Surface A, 2:Surface B
		When the memory allocation setting is "entire area (overwrite)"
			Fixed as 1
		When the memory allocation setting is "entire area (do not overwrite)"
			0: Acrive surface, surface specification (1 to 999)

		dwStartNo
		---------
		The data number to start reading. The first storage data entry number is 0.

		dwStatCnt
		---------
		The number of items to read.
		"""
		_fields_ = [
			("reserve", c_ubyte * 4),
			("dwSurface", c_uint), 
			("dwStartNo", c_uint),
			("dwDataCnt", c_uint)]

	class LJV7IF_STORAGE_INFO(Structure):
		"""
		Parameter Definitions:

		byStatus
		--------
		Storage Status
		0:	Empty (Takes on this value when the target surface has not operated even once in a program with storage on)
		1:	There is still space to store data in the internal memory.
		2:	The internal memory is full and data cannot be stored.

		byProgramNo
		-----------
		The program number for the relevant storage surface

		byTarget
		--------
		Storage target.
		0:	Data storage
		2:	Profile storage
		3:	Batch profile storage
		However, when batch measuremnts are on and profile compression (time axcis) is on, 2: profile storage is stored

		dwStorageCnt
		------------
		Storage count (catch count when batch is on)
		"""
		_fields_ = [
			("byStatus", c_ubyte),
			("byProgramNo", c_ubyte), 
			("byTarget", c_ubyte),
			("reserve", c_ubyte * 5),
			("dwStorageCnt", c_uint)]

	class LJV7IF_GET_STORAGE_RSP(Structure):
		"""
		Paramter Definitions:

		dwStartNo
		---------
		The data number to start reading.

		dwDataCnt
		---------
		The number of items to read

		stBaseTime
		----------
		Base time.
		"""

		class LJV7IF_TIME(Structure):
			"""
			Paramter Definitions:

			byYear
			---
			Year. Set from 0 to 99, which means 2000 to 2099

			byMonth
			-------
			Month. 1 to 12

			byDay
			-----
			Day. 1 to 31

			byHour
			------
			Hour. 0 to 23

			byMinute
			--------
			Minute. 0 to 59

			bySecond
			--------
			Second. 0 to 59
			"""

			_fields_ = [
				("byYear", c_ubyte),
				("byMonth", c_ubyte), 
				("byDay", c_ubyte),
				("byHour", c_ubyte),
				("byMinute", c_ubyte), 
				("bySecond", c_ubyte),
				("reserve", c_ubyte * 2)]

		_fields_ = [
			("dwStartNo", c_uint),
			("dwDataCnt", c_uint), 
			("stBaseTime", LJV7IF_TIME)]

