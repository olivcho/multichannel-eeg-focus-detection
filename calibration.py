"""
The physical voltage range of the MCP3912 ADC in the Ganglion is -15686uV to 15686uV.
A signed 24-bit integer can hold a range of values from -8388608 to 8388607 (MSB holds the sign bit).

To convert the ADC reading to voltage, we need to divide the ADC reading by the scale factor.
The scale factor is the physical voltage range divided by the range of the signed 24-bit integer.
"""
SCALE_FACTOR = 0.001869917138805
fs = 200
ACCELERATION_SCALE_FACTOR = 0.032

FREQUENCY_BANDS = {
    "DELTA": (0.5, 4),
    "THETA": (4, 8),
    "ALPHA": (8, 13),
    "BETA": (13, 30),
    "GAMMA": (30, 99)
}