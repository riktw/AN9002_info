# AN9002_info
Info and a logging script for the AN9002 multimeter

This has just been tested on 1 multimeter. You might need to change the address in the python scripts.

## Usage

To run, the keyboard and bleak libraries need to be installed using:


pip install keyboard

pip install bleak


This script needs to be run as root on Linux due to the keyboard library.

Run the script. After a few seconds it should connect and start showing a graph.
Pressing "q" inside the terminal stops the script and stores the data into a csv file. 
If the unit of measurement is changed(going from volt to amp for example), the logging starts again.
Roughly 2.6 measurements are taken per second, so one minute of logging equals around 156 measurements.


More info can be found on the corresponding [blog post.](https://justanotherelectronicsblog.com/?p=930) 
