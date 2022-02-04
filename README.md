# 468plot
Tektronix 468 Storage Oscilloscope Screen Capture

486plot is a python script that can receive waveform plots from the Tektronix 468 Storage Oscilloscope over GPIB and save the data and screenshot of the graphical display to a file. The program connects to the Tektronix 468 oscilloscope via a GPIB interface using the Prologix protocol. This can be a Prologix or AR488 controller and images can be acquired using either the oscilloscope controller or talk only (TON) mode.

Serial and GPIB parameters are configured in the 468plot.conf file.

![screenshot](https://github.com/Twilight-Logic/468plot/blob/main/images/Screenshot.png)

Brief description of functions:


<i>Capture</i>

Captures the display from the Tektronix 468 oscilloscope. The oscilloscope must be set in storage mode by pressing the NORM button. The oscilloscope GPIB address must be set in 468plot.conf. The oscilloscope GPIB interface configuration is set using DIP switches at the rear of the oscilloscope and must be set in controller mode.


<i>Screenshot</i>

Saves a copy of the current waveform graph to a file. The default file format is .png, but .svg and .pdf can also be selected.


<i>Save Plot</i>

Saves the plot currently being displayed to a file. The plot is stored in the form of the RAW oscilloscope data.


<i>Load Plot</i>

Loads a plot data file into the program. The waveform plot and capture parameters are displayed.


<i>Exit</i>

Quit the program.


<b>Configuration</b>

The configuration file is called 468plot.conf and is an INI style file containing at least 3 sections: Default, Serial and GPIB.

<i>Configuring the serial port</i>

The serial parameters are configured in the <i>Serial</i> section of the 468plot.conf file:

[Serial]
port = /dev/ttyUSB0
baud = 115200
timeout = 3
forcedtr = 1

A maximum <i>timeout</i> period of 3 seconds works for Uno, Nano and Mega 2560 boards as it allows time for the board to reset when a connection is made. Other boards such as 32u4 based adapters might work with a much lower timout figure, although less than 0.5 seconds is not recommended.

The <i>forcedtr</i> setting invokes a piece of code that forcibly sets DTR and is neccessary for clone Uno, Nano and Mega boards using the CH340 UART chip. Setting this to 1 should work for most boards, but some boards (e.g. 32u4) will work just fine with it being set to 0.


<i>Tektronix 468 Controller mode</i>

To operate in controler mode, set oscilloscope GPIB address using the DIP switches next to the controller port and set switch 8 to controller mode. In the 468plot.conf file set the mode to 'ctr', and set the GPIB address of the oscilloscope:

<pre>
[GPIB]
mode = ctr
addr = 17
</pre>

When the <i>Capture</I> button is clicked, the program will connect to the serial interface and establish a connection with the GPIB interface. The interface will be configured for controller mode and the address of the instrument set in the 468plot.conf file, or the default address 1. If the serial port is already open, then this step will be skipped. A read command will then be sent to the oscilloscope which will trigger a capture of the waveform currently on screen. The waveform data is then sent over GPIB to the 468plot program. After a couple of seconds, the waveform and channel data should be displayed in the application window.


<i>Tektronix 468 Talk Only mode</i>

When the oscilloscope is set in talk-only (TON) mode, the interface must be configured for listen-only mode (LON). In this mode, no addressing is required. In the 468plot.conf file, set the mode to 'lon'

<pre>
[GPIB]
mode = lon
</pre>

When the <i>Capture</I> button is clicked, the program will connect to the serial interface and establish a connection with the GPIB interface. The interface will be configured for device mode and listen only mode will be enabled. After a couple of seconds, the prompt to 'Press TRANSMIT....' should appear in the left side text window. The program is now ready to receive data. Pressing the 'Transmit' button on the oscilloscope will trigger a capture of the waveform currently on screen and send the waveform data to the 468plot program. After a couple of seconds, the waveform and channel data should be displayed in the application window.


