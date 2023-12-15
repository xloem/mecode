
[`g.omni_intensity()`](/mecode/api-reference/mecode/#mecode.main.G.omni_intensity) can be used to set the intensity of a Omnicure S2000. [`g.omni_on()`](/mecode/api-reference/mecode/#mecode.main.G.omni_on) and [`g.omni_off()`](/mecode/api-reference/mecode/#mecode.main.G.omni_off) is then used to turn on and off the UV light, respectively.

## Example: UV curing on-the-fly

```python

from mecode import G

g = G()

com_ports = {
    'uv': 1, # UV Omnicure COM PORT
    'P': 5   # Pressure controller COM PORT
}


# define length of a single extruded filament
L = 50 # mm

# Print height
dz = 1 # mm

# set print speed in mm/s
g.feed(10)

# move nozzle to initial printing height
g.move(z=dz)

# Print path strategy
#   1. turn on pressure supply to start printing
#   2. turn on UV after a 5 second delay
#   3. print a single filament of length `L`
#   4. turn off pressure supply to stop printing
#   5. turn of UV
# turn pressure on (e.g., to start printing)
g.toggle_pressure(com_port=com_ports['P']) # ON
g.omni_intensity(com_port=com_ports['uv'], value=50)
g.omni_on(com_port=com_ports['uv'])
g.dwell(5)

g.move(x=L)

g.toggle_pressure(com_port=com_ports['P']) # OFF
g.omni_off(com_port=com_ports['uv'])



g.teardown()

g.view('2d')

```

??? example "Generated gcode"

    ```
    Running mecode v0.2.38
        
    G1 F10
    G1 Z1.000000
    Call togglePress P5
    $strtask4="SIL504E"
    Call omniSetInt P1
    Call omniOn P1
    G4 P5
    G1 X50.000000
    Call togglePress P5
    Call omniOff P1

    Approximate print time: 
            5.101 seconds 
            0.1 min 
            0.0 hrs
    ```
