'''
Created on May 1, 2013

Energy - Dynamic Pricing

Authored by:  Joseph Riley, Maria Virginia Rodriguez, Colin Watts-Fitzgerald
'''
#loading libraries
import csv

filename = 'DP_usage.csv'

#other global variable definitions
dp = 0
dop = 0
peaklist = [] #peak usage list
offpeaklist = [] #off-peak usage list

#######################################################
#
# Read Data
# The following function will read in a csv and parse into a dictionary.
# We will extract out hour and usage key-value pairs and calculate peak and off-peak usage
#
#######################################################
def readData(filename):
    
    global dp, dop
    
    #empty list creation
    rawdata = []
    usagelist = []

    reader = csv.DictReader(open(filename))
    
    #reading raw data - conversion to float on usage for calculations
    for row in reader:
        row['Usage (MWh)'] = float(row['Usage (MWh)'].replace(',',''))
        row['Hour'] = int(row['Hour'])
        rawdata.append(row)
        usagelist.append(row['Usage (MWh)'])
    print rawdata
    #generate summed dp and dop values for peak and off-peak usage
    for i in range(len(rawdata)):
        hour = rawdata[i]['Hour']    
        if (hour >= 10 and hour <=17):
            peaklist.append(rawdata[i]['Usage (MWh)'])
            dp = dp + rawdata[i]['Usage (MWh)']
        else:
            offpeaklist.append(rawdata[i]['Usage (MWh)'])
            dop = dop + rawdata[i]['Usage (MWh)']
    
    return usagelist, peaklist, offpeaklist, dp, dop
#read data end

######################################
#
# Load Redistribution
# This function will redistribute the peak load reduction under the new curve
######################################

def load_redistribution(xp, xop):
    global peaklist 
    global offpeaklist
    global dp, dop
    
    Ratio = xp/xop
    Lv =(1- (Ratio-1)^0.441066/100)
    Gv = Ratio^(-0.2133333)
    New_peak_load = []
    New_off_peak_load = []
    for item in peakusage:
        New_peak_load.append(Lv*item)
    up = sum(New_peak_load)
    uop = up/((Dp/Dop)*Gv) 
    Percentage = uop/Dop
    for item in offpeakusage:
        New_off_peak_load.append((Percentage)*item)
    
    return New_peak_load, up
#load distribution end




####################################3
#
# Function Calls
#
#####################################

readData(filename)
print dp
print dop
print peaklist
print offpeaklist


