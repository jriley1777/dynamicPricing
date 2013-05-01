'''
Created on 01/05/2013

@author: mariavirginiarodriguez
'''
import matplotlib.pyplot as plt



peakusage = []
offpeakusage = []
Dp, Dop

def load_redistribution(xp, xop):
    ''' This functions redistributes the maximum load'''
    global peakusage 
    global offpeakusage
    global Dp, Dop
    
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