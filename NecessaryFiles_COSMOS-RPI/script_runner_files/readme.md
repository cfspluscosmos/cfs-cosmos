Hello User!

You should place the folder log_app under the cosmosdemo folder and the file log_app_generator.rb under the cosmosdemo/procedures folder. 

Load the log_app_generator.rb at the cosmos script runner (after you have stated the telemetry server) and voilà! You have a little file with just the items at the configure being shown up! 

Config.txt structure:

First line: target
Second line: interval that the log file will receive more items from telemetry
Third line: the name of the items that will be recorded in the log file 
