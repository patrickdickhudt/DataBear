'''
Simulated Streaming Sensor
A test module for a generic streaming sensor. 
- Platform: Windows, Linux
- Tested hardware: USB-RS485 (loopback), Dyacon MDL serial module
- Interface: DataBear Sensor Interface V0
'''

import datetime
import serial
import re
from databear import ReadLine
import pdb

class maxBotixAlt:
    def __init__(self,name,settings):
        '''
        Abstract class for a streaming sensor
        Inputs
            - settings['serialnumber']
            - settings['port']
            - settings['baud']
            - settings['hz'] - Data stream frequency from sensor
        '''
        #Define characteristics of this sensor
        self.sensor_type = 'continuous'

        #Load sensor settings
        self.name = name
        self.sn = settings['serialnumber']
        self.port = settings['port']
        self.baud = settings['baud']
        self.timeout = 1
        self.maxfrequency = 0.1  #Maximum frequency in seconds the sensor can be polled
        
        #Serial settings
        self.rs = 'RS232'
        self.duplex = 'half'
        self.resistors = 0
        self.bias = 0

        #Set up connection
        self.comm = serial.Serial(self.port,self.baud,timeout=self.timeout)
        self.comm.flushInput()  # flush input buffer so getting current data
        #Define measurements
        self.data = {'range':[]}  # this data name should come from store in datalogger
        self.dataRE = re.compile('\d\d\d\d')
        
    def measure(self):
        '''
        Read in data from port and parse to measurements
        '''
        
        vals = None
        while not vals:
            dt = datetime.datetime.now()    
            timestamp = dt.strftime('%Y-%m-%d %H:%M:%S %f')
            rawdata = self.comm.read_until(b'\r').decode('utf-8')
            
            #print('rawdata: {}'.format(rawdata))            
            vals = re.findall(self.dataRE,rawdata) #Search for matches in rawdata
        vals = vals[0]
        valsOut = [timestamp,vals]
        
        self.data['range'].append((dt,valsOut))
        
    def getdata(self,name,startdt,enddt):
            '''
            Return a list of values such that
            startdt <= timestamps < enddt
            - Inputs: datetime objects
            '''
            output = []
            data = self.data[name]
            for val in data:
                #if (val[0]>=startdt) and (val[0]<enddt):  # this results in a lot of streaming data to be lost. 
                output.append(val)
            return output
        
    def cleardata(self,name):
        '''
        Clear data values for a particular measurement
        '''
        self.data[name] = []

