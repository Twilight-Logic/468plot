#!/usr/bin/python3

# Tektronix 468 oscilloscope plot decoder
# Version 0.01.17 
# Twilight Logix, @16/01/2022
# Dependencies:
# matplotlib, numpy
# matplotlib, numpy
# Also uses: Tkinter, pyserial


import configparser
import serial
import time
import tkinter as tk
import matplotlib.pyplot as plt
import numpy as np

from tkinter import filedialog
from tkinter import messagebox
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter, AutoMinorLocator)
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)


def main():
  ys = -4
  ye = 4
  ym = 1
  xs = 0
  xe = 10
  xm = 1
  global window, fig, ax
  lab_title = tk.Label(master=window, text="Tektronix 468 Storage Oscilloscope Waveform Capture", font=("Helvetica", 18) )
  lab_title.place(x=220, y=20)
  lab_credit = tk.Label(master=window, text="(c) Twilight Logic, 14/10/2022, version 0.01.17")
  lab_credit.place(x=360, y=50)

  fig.patch.set_facecolor('PaleGreen')
  ax.set_facecolor("black")
  ax.grid(color='#2A2A2A', linestyle='-', linewidth=0.7)

  # Suppress display of axis labels
  ax.xaxis.set_ticklabels([])
  ax.yaxis.set_ticklabels([])

  # X and Y axis major and minor ticks
  ax.set_xticks(np.arange(xs,xe,xm))
  ax.set_yticks(np.arange(ys,ye,ym))
  ax.xaxis.set_minor_locator(MultipleLocator(xm/5))
  ax.yaxis.set_minor_locator(MultipleLocator(ym/5))

  # X and Y axis limits
  ax.set_xlim([xs,xe])
  ax.set_ylim([ys,ye])


  # Axis location in centre (top and bottom required for ticks both sides)
  ax.spines['left'].set_position('center')
  ax.spines['right'].set_position('center')
  ax.spines['bottom'].set_position('center')
  ax.spines['top'].set_position('center')

  # Axis colour (left and right required for ticks both sides)
  ax.spines['left'].set_color('grey')
  ax.spines['right'].set_color('grey')
  ax.spines['top'].set_color('grey')
  ax.spines['bottom'].set_color('grey')

  # Enable major ticks and set color ('which=both' changes both major and minor ticks)
  ax.tick_params(axis='x', which='both', colors='grey', top=True, bottom=True)
  ax.tick_params(axis='y', which='both', colors='grey', left=True, right=True)

  canvas = FigureCanvasTkAgg(fig, master=window)
  canvas.draw()

#  toolbar = NavigationToolbar2Tk(canvas, window)
#  toolbar.update()
  canvas.get_tk_widget().place(x=330, y=90)

  txt_output = tk.Text(master=window, width=30, height=28, borderwidth=2, relief="flat", font=("monospace",10))
  txt_output.place(x=50, y=90)
  txt_output.configure(bg='SpringGreen')
  txt_output.bind("<Key>", lambda e: "break")


  frm_controls = tk.Frame(master=window, width=610, height=50)

  btn_capture = tk.Button(master=frm_controls, width=8, text="Capture", command=lambda *args: capture_click(canvas, txt_output))
  btn_capture.pack(padx=5, pady=15, side=tk.LEFT)

  btn_screenshot = tk.Button(master=frm_controls, width=8, text="Screenshot")
  btn_screenshot.bind("<Button-1>", screenshot_click)
  btn_screenshot.pack(padx=5, pady=15, side=tk.LEFT)

  btn_save = tk.Button(master=frm_controls, width=8, text="Save Plot")
  btn_save.bind("<Button-1>", save_click)
  btn_save.pack(padx=5, pady=15, side=tk.LEFT)

  btn_load = tk.Button(master=frm_controls, width=8, text="Load Plot", command=lambda *args: load_click(canvas, txt_output))
  btn_load.pack(padx=5, pady=15, side=tk.LEFT)

  btn_close = tk.Button(master=frm_controls, width=8, text="Exit")
  btn_close.bind("<Button-1>", quit_click)
  btn_close.pack(padx=5, pady=15, side=tk.LEFT)

  frm_controls.place(x=400, y=580)

  window.mainloop()

                               
def getYarray(plot, ymult):
  yarray = []
  y = 0

  # Calculate the graph plot point for each byte
  for i in range ( int(plot['psize']) ):

    # Value of byte i
    y = int(plot['pdata'][i])
    # Calculate to absolute value and adjust for mid-point
    # Note: manual says 25 points per division, however byte max = 256 which is 32 points per division
    #       Setting mid-point at 100 (4 x 25) does not center the plot correctly, but 128 (256/2) does.
    #       Therefore a value of 128 was chosen as the mid-point value. The below is a modified
    #       version of the Y axis formula from the manual, but adjusted for centering on mid-point.
#    y = int(plot['YZERO']) + ( int(plot['YMULT']) * (y - 128 - int(plot['YOFF']) ) )
    y = int(plot['YZERO']) + ( ymult * (y - 128 - int(plot['YOFF']) ) )
    yarray.append(y)

  return yarray


def drawPlot(plotdataset):

  xs = 0
  xe = 10
  ys = -4
  ye = 4
  xm = 1
  ym = 1

  # Plot objects
  global fig, ax

  ax.set(title='486 Digital Storage Oscilloscope Waveform\n')
#  plt.figtext(0.3, 0.05, "468plot, Twilight Logic (c) Jan 2022")

  if "pdata" in plotdataset['plots'][0]:

#      print("Plot data passed to Yarray:")
#      print(plotdataset['plots'][key])
#      print("END")

    if "XINCR" in plotdataset['plots'][0]:
      xm = int(plotdataset['plots'][0]['XINCR'])
      xe = 10 * xm
      ym = int(plotdataset['plots'][0]['YMULT']) * 25   # Resolution = 25 data points per division
      ys = ys * ym
      ye = ye * ym

      # X-Axis spacing
      xz = int(plotdataset['plots'][0]['NR.PT'])
      x = np.arange(0.0, xe, xe/xz)

      # Plot labels
      ax.set(xlabel='time (' + plotdataset['plots'][0]['XUNIT'] + ')', ylabel='voltage (' + plotdataset['plots'][0]['YUNIT'] + ')')

      # Suppress display of axis labels
      ax.xaxis.set_ticklabels([])
      ax.yaxis.set_ticklabels([])

      # X and Y axis major and minor ticks
      ax.set_xticks(np.arange(xs,xe,xm))
      ax.set_yticks(np.arange(ys,ye,ym))
      ax.xaxis.set_minor_locator(MultipleLocator(xm/5))
      ax.yaxis.set_minor_locator(MultipleLocator(ym/5))

      # Axis location in centre (top and bottom required for ticks both sides)
      ax.spines['left'].set_position('center')
      ax.spines['right'].set_position('center')
      ax.spines['bottom'].set_position('center')
      ax.spines['top'].set_position('center')

      # Axis colour (left and right required for ticks both sides)
      ax.spines['left'].set_color('grey')
      ax.spines['right'].set_color('grey')
      ax.spines['top'].set_color('grey')
      ax.spines['bottom'].set_color('grey')

      # Enable major ticks and set color ('which=both' changes both major and minor ticks)
      ax.tick_params(axis='x', which='both', colors='grey', top=True, bottom=True)
      ax.tick_params(axis='y', which='both', colors='grey', left=True, right=True)
            
      # X and Y axis limits
      ax.set_xlim([xs,xe])
      ax.set_ylim([ys,ye])

      plotnum = len(plotdataset['plots'])
      ymult = int(plotdataset['plots'][0]['YMULT'])
      for i in range(0,plotnum):

        yarray = bytearray()
        yarray = getYarray(plotdataset['plots'][i], ymult)

        # Plot data
        h, = ax.plot(x, yarray)
        h.set_label(plotdataset['plots'][0]['channel'])

    if len(plotdataset['plots']) == 1:
      ax.legend(bbox_to_anchor=(0.60, -0.02), ncol=2)
    if len(plotdataset['plots']) == 2:
      ax.legend(bbox_to_anchor=(0.68, -0.02), ncol=2)


def redraw_plot(canvas, databox, rawplotdata):
  global plotdataset
  global ax
  if (rawplotdata):
    ax.clear()
    getPlotData(rawplotdata, plotdataset)
    drawPlot(plotdataset)
    updateDataBox(databox, plotdataset)
    canvas.draw()


def quit_click(event):
  plt.close('all')
  quit()


def screenshot_click(event):
  global fig
  fpath = filedialog.asksaveasfilename(filetypes=[("Portable Network Graphics", "*.png"),("Scalable Vector Graphics","*.svg"),("Portable Document Format","*.pdf")], initialfile = "screenshot.png")
  if not fpath:
    return
  else:
    fname, fext = fpath.split('.')
    print("Fname: " + fname)
    print("Fext: " + fext)
    if fext == "png":
      fpath = fname + '.png'
      fig.savefig(fpath, format="png")
    if fext == "svg":
      fpath = fname + '.svg'
      fig.savefig(fpath, format="svg")
    if fext == "pdf":
      fpath = fname + '.pdf'
      fig.savefig(fpath, format="pdf")
  fname


def capture_click(canvas, databox):
  global plotdataset
  global fig, ax
  global rawplotdata
  gpibPlotData = gpibFetchPlotData()
  if (gpibPlotData):
    rawplotdata = gpibPlotData
    redraw_plot(canvas, databox, gpibPlotData)


def load_click(canvas, databox):
  global fig
  global rawplotdata
  fpath = filedialog.askopenfilename(filetypes=[("468 Plot file", "*.468"),("All files","*.*")])
  if fpath:
    plotfiledata = bytearray()
    with open (fpath, 'rb') as plotfile:
      byte = plotfile.read()
      while byte != b'':
        plotfiledata += byte
        byte = plotfile.read()
    plotfile.close()
    rawplotdata = plotfiledata
    if len(plotfiledata) > 0:
      redraw_plot(canvas, databox, plotfiledata)


def save_click(event):
  global rawplotdata
  files = [("468 Plot file", "*.468"),("All files","*.*")]
  file = filedialog.asksaveasfile(mode = 'wb', filetypes = files, defaultextension = files, initialfile="plotdata.468")
  if file == None:
    return
  file.write(rawplotdata)
  file.close()


def decodeID(idstring, plot):
  param = []

  idlist = idstring.split(',')
  param = idlist[0].split(' ')
  plot['devid'] = param[1]

  plot['dver'] = idlist[1]

  param = idlist[2].split(':')
  plot['fwver'] = param[1]


def decodeParams(paramstr, plot):
  paramlist = paramstr.split(',')
  wfmid = paramlist[0].split(':')
  chaninfo = wfmid[1].strip('"').split(' ')
  cnt = 0
  
  plot['channel'] = chaninfo[0]
  plot['coupling'] = chaninfo[1]

  for line in paramlist:
    if ( (cnt>0) and (line != "") ):
      param = line.split(':')
      plot[param[0]] = param[1]
    cnt += 1


def decodePlotData(plotarray, plot):
  psize = (plotarray[0] * 256) + plotarray[1] - 1
  plot['psize'] = psize
  plot['pdata'] = plotarray[2:(psize+2)]
  plot['pchk'] = plotarray[(psize+2)]
    

def loadPlotDataFile(plot_file_name, plotdataset):
  devidstr = ""
  params = ""
  byte = ''
  bytecnt = 0
  pcnt = 1
  plots = []
  readbytes = 0

  with open (plot_file_name, 'rb') as plotfile:

    # Read the ID string
    byte = plotfile.read(1)
    while byte != b";":
      devidstr += byte.decode()
      byte = plotfile.read(1)
    decodeID(devidstr, plotdataset)

#    print("Read ID")

    # Read the parameters string
    byte = plotfile.read(1)
    while (byte != b""):
      if (byte != b"%"):
        params += byte.decode()
      else:
        plot = {}
        plotdata = bytearray()
        decodeParams(params, plot)
        readbytes = int(plot['NR.PT']) + 4
        for i in range (readbytes):
          byte = plotfile.read(1)
          plotdata += byte
          bytecnt += 1
        decodePlotData(plotdata, plot)

#        print("Read plot data " + str(pcnt))
#        print(plot)

        plots.append(plot)

        params = ""
        pcnt += 1

      byte = plotfile.read(1)

 
#    print("Read all plot data.")

#    print("ALL plots: ")
#    print(plots)
#    print("END")
  
  plotfile.close()  
  plotdataset['plots'] = plots

#  print("END of read")


def getPlotData(GPIBdata, plotdataset):
  pdlen = len(GPIBdata)
  pdcnt = 0
  devidstr = ""
  params = ""
  byte = ''
  pcnt = 1
  plots = []
  readbytes = 0

  # Read the ID string
  while chr(GPIBdata[pdcnt]) != ";":
    devidstr += chr(GPIBdata[pdcnt])
    pdcnt += 1
  decodeID(devidstr, plotdataset)

#  print("Read ID")

#  print("PdCnt: " + str(pdcnt))
#  print("PdLen: " + str(pdlen))


  # Read the parameters string
  while (pdcnt < pdlen):
    if (chr(GPIBdata[pdcnt]) != "%"):
      params += chr(GPIBdata[pdcnt])
    else:
      plot = {}
      plotdata = bytearray()
      decodeParams(params, plot)
      readbytes = int(plot['NR.PT']) + 4
      for i in range (readbytes):
        pdcnt +=1
        plotdata.append(GPIBdata[pdcnt])
      decodePlotData(plotdata, plot)

#      print("Read plot data " + str(pcnt))
#      print(plot)

      plots.append(plot)

      params = ""
      pcnt += 1

    pdcnt += 1

 
#  print("Read all plot data.")

#  print("ALL plots: ")
#  print(plots)
#  print("END")
  
  plotdataset['plots'] = plots

#  print("END of read")


def updateDataBox(databox, plotmeta):

  databox.delete(1.0, tk.END)
  databox.insert(1.0, "Device information:\n\n")
  databox.insert(tk.END, "Device type:    " + plotmeta['devid'] + "\n")
  databox.insert(tk.END, "GPIB C&F ver:   " + plotmeta['dver'] + "\n")
  databox.insert(tk.END, "F/W version:    " + plotmeta['fwver'] + "\n")

  databox.insert(tk.END,"\nPlot parameters:\n\n")

  plotnum = len(plotmeta['plots'])
  for i in range(0,plotnum):
    databox.insert(tk.END, "Channel:        " + plotmeta['plots'][i]['channel'] + "\n")  # CH1, CH2, ADD
    databox.insert(tk.END, "Coupling:       " + plotmeta['plots'][i]['coupling'] + "\n") # AC, DC, GND, UNK
    databox.insert(tk.END, "Plot points:    " + plotmeta['plots'][i]['NR.PT'] + "\n")    # 256/512
#    databox.insert(tk.END, "Point format:   " + plotmeta['plots'][i]['PT.FMT'] + "\n")   # Y = y-coord transmitted, X = data point number
    databox.insert(tk.END, "Trigger point:  " + plotmeta['plots'][i]['PT.OFF'] + "\n")   # Trigger point 32, 64, 224, 448
    databox.insert(tk.END, "X increment:    " + plotmeta['plots'][i]['XINCR'] + "\n")    # increment x units = time between points
    databox.insert(tk.END, "X units:        " + plotmeta['plots'][i]['XUNIT'] + "\n")    # X unit of measure
    databox.insert(tk.END, "Y multiplier:   " + plotmeta['plots'][i]['YMULT'] + "\n")    # Y mulitplier/scaling volts/div (units per data point)
    databox.insert(tk.END, "Y offset:       " + plotmeta['plots'][i]['YOFF'] + "\n")     # Vertical position ground reference
    databox.insert(tk.END, "Y units:        " + plotmeta['plots'][i]['YUNIT'] + "\n")    # V, MV, UV, DIV
#    databox.insert(tk.END, "Encoding:       " + plotmeta['plots'][i]['ENCDG'] + "\n")    # ENCDG:BIN - low level binary code
#    databox.insert(tk.END, "Binary format:  " + plotmeta['plots'][i]['BN.FMT'] + "\n")   # BN:FMT:RP - each byte is a binary positive number
    databox.insert(tk.END, "\n")


def printPlotData(plot):
  print("\nDevice information:")
  print("Device type:    " + plot['devid'])
  print("GPIB C&F ver:   " + plot['dver'])
  print("F/W version:    " + plot['fwver'])

#  print(plot['plots']['1'])

  plotnum = len(plot['plots'])
  for i in range(0,plotnum):
    print("Idx: " + str(i))
    print("\nPlot parameters:")
    print("Channel:        " + plot['plots'][i]['channel'])  # CH1, CH2, ADD
    print("Coupling:       " + plot['plots'][i]['coupling']) # AC, DC, GND, UNK
    print("Plot points:    " + plot['plots'][i]['NR.PT'])    # 256/512
    print("Point format:   " + plot['plots'][i]['PT.FMT'])   # Y = y-coord transmitted, X = data point number
    print("X increment:    " + plot['plots'][i]['XINCR'])    # increment x units = time between points
    print("X origin:       " + plot['plots'][i]['XZERO'])    # X origin = zero
    print("Point offset:   " + plot['plots'][i]['PT.OFF'])   # Trigger point 32, 64, 224, 448
    print("X units:        " + plot['plots'][i]['XUNIT'])    # X unit of measure
    print("Y multiplier:   " + plot['plots'][i]['YMULT'])    # Y mulitplier/scaling volts/div (units per data point)
    print("Y origin:       " + plot['plots'][i]['YZERO'])    # Y origin = zero
    print("Y offset:       " + plot['plots'][i]['YOFF'])     # Vertical position ground reference
    print("Y units:        " + plot['plots'][i]['YUNIT'])    # V, MV, UV, DIV
    print("Encoding:       " + plot['plots'][i]['ENCDG'])    # ENCDG:BIN - low level binary code
    print("Binary format:  " + plot['plots'][i]['BN.FMT'])   # BN:FMT:RP - each byte is a binary positive number
    print("Bytes per num.: " + plot['plots'][i]['BYT/NR'])   # BYT/NT:1 - Bytes per number = 1
    print("Bits per num.:  " + plot['plots'][i]['BIT/NR'])   # BIT/NR:8 - eight bits per byte  

    print("\nPlot data:")
    print("Plot data size: " + str(plot['plots'][i]['psize']))
    print("Checksum:       " + str(plot['plots'][i]['pchk']))  
#    print("\nPlot data:")
#    print(plot['plots'][i]['pdata'])


def gpibFetchPlotData():
  global cfg
  addrcmd = ""

  print("Opening serial port...")

  # Configure and open serial port
  ser = serial.Serial()
  ser.port = cfg['Serial']['port']
  ser.baudrate = int(cfg['Serial']['baud'])
  ser.timeout = float(cfg['Serial']['timeout'])
  ser.open()

  if (ser.is_open):
    ser.write(b'++ver\n')
    version = ser.readline().decode()
    if "GPIB-USB" in version:
      print(version)

#      print("Configuring GPIB...")
      time.sleep(0.2)
      # Set up GPIB interface
      ser.write(b'++mode 1\n')
#      print(str(cfg['GPIB']['addr']))#gpibPlotData = gpibFetchPlotData()
      addrcmd = "++addr " + str(cfg['GPIB']['addr']) + "\n"
      ser.write(addrcmd.encode())


#      print("Sending ++mode...")
#      ser.write(b'++mode\n')

#      print("Reading reply...")
#      mode = ser.readline().decode()
#      print ("Mode: " + mode)

#      print("Sending ++addr...")
#      ser.write(b'++addr\n')

#      print("Reading reply...")
#      addr = ser.readline().decode()
#      print("Addr: " + addr)

      print("Fetching plot data...")
      time.sleep(0.2)

      # Read scope data
      plotdata = bytearray()
      ser.write(b'++read\n')
      bytesToRead = 0

      byte = ser.read(1)
      while ( byte != b"" ) :
        plotdata += byte
        byte = ser.read(1)

#      print(plotdata)

      ser.close()
      return plotdata

    else:
      print("GPIB interface not found!")
      ser.close()

  else:
    print("Failed to open the serial port!")

  return None


def setDefaultSerialConfig(cfg):
  cfg['Serial']['port']  = '/dev/ttyUSB0'
  cfg['Serial']['baud'] = 9600
  cfg['Serial']['timeout'] = 0
  cfg['GPIB']['addr'] = 1


def readConfigFile(config, cfg):
  config.read(r'468plot.conf')
  try:
    # Serial port configuration
    if ('port' in config['Serial']) :
      cfg['Serial']['port'] = config['Serial']['port']
    if ('baud' in config['Serial']) :
      cfg['Serial']['baud'] = config['Serial']['baud']
    if ('timeout' in config['Serial']) :
      cfg['Serial']['timeout'] = config['Serial']['timeout']

    # GPIB configuration
    if ('addr' in config['GPIB']) :
      cfg['GPIB']['addr'] = config['GPIB']['addr']
  except:
    print("Error reading config file!")



# Main application window
window = tk.Tk()
window.title('Tektronix 468 Storage Oscilloscope Image Capture')
window.geometry("1024x650")

# Plot window
fig, ax = plt.subplots()


# Configuration reader object
config = configparser.ConfigParser()
# Set default configuration
cfg = {'Default':{}, 'Serial':{}, 'GPIB':{}}
setDefaultSerialConfig(cfg)

# Read configuration file
readConfigFile(config, cfg)

# Structure to hold the plot data
plotdataset = {}
rawplotdata = bytearray()

main()




#plotfile = "Tek768.dat"

#plotfile = "sample1-wave.dat"
#plotfile = "sample2-am.dat"
#plotfile = "sample3-stair.dat"
#plotfile = "sample4-dual1.dat"
#plotfile = "sample5-dual2.dat"
#plotfile = "sample6-wave2.dat"
#plotfile = "sample7-wavec.dat"

#

#gpibPlotData = gpibFetchPlotData()



#if (plotfile):
#  loadPlotDataFile(plotfile, plotdataset)
#  print(plotdataset)
#  printPlotData(plotdataset)
#  drawPlot(plotdataset)

#if (gpibPlotData):
#  print(gpibPlotData)
#  getPlotData(gpibPlotData, plotdataset)
#  print(plotdataset)
#  printPlotData(plotdataset)
#  drawPlot(plotdataset)

fig.close()
window.close()

