import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, RangeSlider

def GetParams(Waveform):
    # As input: Waveform = np.array([time],[Voltage]), recommended to use averaged.
    # Opens a graphical interface to choose the signal area and offset.
    
    # Create an array for the offset.
    maxV = max(abs(Waveform[1]))
    minV = min(abs(Waveform[1]))
    offset = np.array(Waveform[1])*0+maxV
    
    fig, ax = plt.subplots()
    
    plt.subplots_adjust(left=0.25, bottom=0.25) # Make space for the sliders
    
    # Plot Waveform and offset line
    ax.plot(Waveform[0],Waveform[1])
    baseline, = ax.plot(Waveform[0],offset)
    peak, = ax.plot(Waveform[0],offset-maxV+minV)
    HM, = ax.plot(Waveform[0],(offset+minV)/2)
    FWHM0, = ax.plot([500,500],[minV-10,maxV+10])
    FWHM1, = ax.plot([630,630],[minV-10,maxV+10])
    
    # Set the starting t limits to fit the full dataset
    tlims = [Waveform[0][0], Waveform[0][-1]]
    ax.set_xlim(*tlims)
    
    # Create a plt.axes object to hold the slider [left,bottom,width,height]
    Xrange_ax = plt.axes([0.2, 0.12, 0.65, 0.05])
    baseline_ax = plt.axes([0.03, 0.25, 0.04, 0.63])
    peak_ax = plt.axes([0.12, 0.25, 0.04, 0.63])
    
    # Add slider to adjust 
    XRange_Slider = RangeSlider(Xrange_ax, "Signal area", valmin = Waveform[0][0], valmax = Waveform[0][-1])
    XRange_Slider.set_val((500,630))
    
    # Add slider to adjust offset
    baseline_Slider = Slider(baseline_ax, "Baseline", valmin = 0.9*maxV, valmax = 1.1*maxV, valinit=maxV,orientation ="vertical")
    peak_Slider = Slider(peak_ax, "Peak", valmin = 0.9*minV, valmax = 1.1*minV, valinit=minV,orientation ="vertical")
    
    # Define functions to run whenever the slider changes its value and change graph accordingly.
    def baselineupdate(val):
        baseline.set_ydata(baseline_Slider.val)
        peak.set_ydata(peak_Slider.val)
        HM.set_ydata((peak_Slider.val+baseline_Slider.val)/2)
        fig.canvas.draw_idle()
    
    def FWHMupdate(val):
        FWHM0.set_xdata([val[0],val[0]])
        FWHM1.set_xdata([val[1],val[1]])
        fig.canvas.draw_idle()
    
    # Register the function update to run when the slider changes value
    XRange_Slider.on_changed(FWHMupdate)
    baseline_Slider.on_changed(baselineupdate)
    peak_Slider.on_changed(baselineupdate)
    
    plt.show()

    # Return FWHM ([x1,x2]), middlepoint ((x1+x2)/2), baseline (y)
    return [XRange_Slider.val.tolist(),(XRange_Slider.val[0]+XRange_Slider.val[1])/2 , baseline_Slider.val]