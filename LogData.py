import sys
import asyncio
import platform
import logging
import keyboard
import csv

from multimeter import *
import matplotlib.pyplot as plt
from bleak import BleakClient

ADDRESS = (
    "FC:58:FA:3C:94:16"
)

CHARACTERISTIC_UUID = "0000fff4-0000-1000-8000-00805f9b34fb"  # <--- Change to the characteristic you want to enable notifications from.

dataGraph = []
multimeter = AN9002()
lastDisplayedUnit = ""

def notification_handler(sender, data):
    global dataGraph
    global multimeter
    global lastDisplayedUnit
    """Simple notification handler which prints the data received."""
    #print("Data multimeter: {0}".format(data.hex(' ') ))
    multimeter.SetMeasuredValue(data)
    displayedData = multimeter.GetDisplayedValue()
    if multimeter.overloadFlag:
        displayedData = 99999
        print("Overload")
    
    unit = multimeter.GetDisplayedUnit()
    if lastDisplayedUnit == "":
        lastDisplayedUnit = unit
    
    if unit != lastDisplayedUnit:
        lastDisplayedUnit = unit
        dataGraph.clear()
        plt.clf()
    
    dataGraph.append(displayedData)
    plt.ylabel(unit)
    print(str(displayedData) + " " + unit) 
     

async def run(address):
    client = BleakClient(address)
        
    try:
        await client.connect()
        await client.start_notify(CHARACTERISTIC_UUID, notification_handler)

        while(1):
            if keyboard.is_pressed("q"):
                print("Shutting down!");
                break;
            else:
                plt.plot(dataGraph, color='b')
                plt.draw()
                plt.pause(0.1)
                await asyncio.sleep(0.5)       
            
    except Exception as e:
        print(e)
    finally:
        await client.stop_notify(CHARACTERISTIC_UUID)
        await client.disconnect()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.set_debug(False)
    loop.run_until_complete(run(ADDRESS))
    
    with open('plot.csv', 'w') as f:
        wr = csv.writer(f)
        wr.writerow(dataGraph)
    
