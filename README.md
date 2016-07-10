# CFS-Cosmos
How to communicate CFS (Core Flight System) and Cosmos Ball Aerospace

This is a new version of CFS-Cosmos 2015 project. The main differences are pointed out below.

## At CFS
The telemetry frame changed. Now it is: frame count, time at the Raspberry Pi (PiSat), light sensor data, temperature sensor data, command count and checksum. <br />
The files that changed are:<br />
  1. sensors.py at FlatSat tool: frame count, time at pi and command count were introduced and then added to the telemetry packet.
  2. cmdUtil.c at cmdUtil tool: the checksum is computed here, then added to packet as well.

## At Cosmos
Main differences at Cosmos files are due to: read the new telemetry data and a new approach to make log and send relevant information to a database.<br />
The files that changed are:<br />
  1. Under <cosmos folder>/config/targets/RPI:
   * target.txt: require any new ruby code necessary to conversion of data, in this case, conversion_timestamp.rb.
   * Under lib, conversion_timestamp.rb was added.
   * Under cmd_tlm, any new item is pointed in rpi_tlm.txt. 
   * Under screens, any new item is pointed in tlm.txt.
  2. Script Runner is used instead of Telemetry Extractor:
   * There is now a log_app folder: it has the config.txt file, and the log files are going to created here.
   * Under <cosmos_folder>/procedures, log_app_generator was added.
