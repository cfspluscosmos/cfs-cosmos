# CFS-Cosmos
How to communicate CFS (Core Flight System) and Cosmos Ball Aerospace

This is a new version of CFS-Cosmos 2015 project. The main differences are pointed out below.

# At CFS
The telemetry frame changed. Now it is: frame count, time at the Raspberry Pi (PiSat), light sensor data, temperature sensor data, command count and checksum. <br />
The files that changed are:
1. sensors.py at FlatSat tool: frame count, time at pi and command count were introduced and then added to the telemetry packet.
2. cmdUtil.c at cmdUtil tool: the checksum is computed here, then added to packet as well.

# At Cosmos
