#Energy - Dynamic Pricing

#Authored by:  Joseph Riley, Maria Virginia Rodriguez, Colin Watts-Fitzgerald

#loading libraries
import csv
import numpy as np

#file path
filename = "DP_usage.csv" ##Change path here if not in current workspace

#other global variable definitions
dp = 0
dop = 0
peaklist = [] #peak usage list
offpeaklist = [] #off-peak usage list
flat_rate=90 #90 dollars per MWH

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
#
######################################

def load_redistribution(xp, xop):
    global peaklist 
    global offpeaklist
    global dp, dop, up, uop, New_peak_load, New_off_peak_load
    
    #redistribute loads for peak and offpeak times
    #Lv,Gv,Qv are our functions identifying load shifts, usage ratios, and elasticity
    
    Ratio = xp/xop
    Lv=1-((np.power((Ratio-1),0.441066))/100)
    Gv=np.power(Ratio,-0.2133333)
    Qv=np.power(Ratio,-0.016033333)
    New_peak_load = []
    New_off_peak_load = []
    
    #This loop calculates our percentage shift from our Dp to the new load during each hour and then calculates up
    for item in peaklist:
        New_peak_load.append(Lv*item)
    up = sum(New_peak_load)
    uop = ((dp+dop)*Qv)/(1+(dp/dop)*Gv) 
    
    #this loop uses our combined equations of Gv and Qv to find the shift as a ratio of our Dop to the new load during each hour
    for item in offpeaklist:
        New_off_peak_load.append((uop)*(item/dop))
    
    return New_peak_load, New_off_peak_load, up, uop
#load distribution end

#####################################
#
# Finding Peak price when given off peak price using bill neutrality
# function calculating xp (peak price) from being given xop (off peak price) and bill neutrality
#
#####################################

def peak_price(xop):
    global xp
    
    xp=((dp+dop)*flat_rate-dop*xop)/dp
    
    return xp

#####################################
#
# Function Calls
#
#####################################

readData(filename)
print dp
print dop
print peaklist
print offpeaklist

load_redistribution(120,.70) #test
print New_peak_load
print New_off_peak_load
print up
print uop

peak_price(70) #test
print xp