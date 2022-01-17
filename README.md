# 468plot
Tektronix 468 Storage Oscilloscope Screen Capture

486plot is a python script that can receive waveform plots on the Tektronix 468 Storage Oscilloscope over GPIB and save the data to a file as well as create a screenshot of the graphical display.

The program connects to the Tektronix 468 over GPIB. Cuttently it interfaces with a Prologix or AR488 controller only and operates in controller mode. Talk only mode is not yet supported.

Serial and GPIB parameters are configured in the 468plot.conf file.

![screenshot](https://github.com/Twilight-Logic/468plot/blob/main/images/Screenshot.png)

Brief description of functions:


Capture

Captures the display from the Tektronix 468 oscilloscope. The oscilloscope must be set in storage mode by pressing the NORM button. The oscilloscope GPIB address must be set in 468plot.conf. The oscilloscope GPIB interface configuration is set using DIP switches at the rear of the oscilloscope and must be set in controller mode.


Screenshot

Saves a copy of the current waveform graph to a file.


Save Plot

Saves the plot currently being displayed to a file. The plot is stored in the form of the RAW oscilloscope data.


Load Plot

Loads a plot data file into the program. The waveform plot and capture parameters are displayed.


Exit

Quit the program.
