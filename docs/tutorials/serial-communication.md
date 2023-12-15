## Direct control via serial communication

With the option `direct_write=True`, a serial connection to the controlled device 
is established via USB serial at a virtual COM port of the computer and the 
g-code commands are sent directly to the connected device using a serial 
communication protocol:

```python
import mecode

g = mecode.G(
    direct_write=True, 
    direct_write_mode="serial", 
    printer_port="/dev/tty.usbmodem1411", 
    baudrate=115200
)
# Under MS Windows, use printer_port="COMx" where x has to be replaced by the port number of the virtual COM port the device is connected to according to the device manager.

g.write("M302 S0")  # send g-Code. Here: allow cold extrusion. Danger: Make sure extruder is clean without filament inserted 

g.absolute()  # Absolute positioning mode

g.move(x=10, y=10, z=10, F=500)  # move 10mm in x and 10mm in y and 10mm in z at a feedrate of 500 mm/min

g.retract(10)  # Move extruder motor

g.write("M400")  # IMPORTANT! wait until execution of all commands is finished

g.teardown()  # Disconnect (close serial connection)
```