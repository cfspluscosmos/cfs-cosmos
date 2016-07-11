# This code will generate a log file to be exported to the app 
# Project: coSPIC
# Author: Aryadne Rezende  
# Date: 07/07/2016
# Contact: aryadneccomp@gmail.com
require 'net/http'
require 'uri'
require 'json'

#load the generate_log_app variables from the config file
def load_vars()
  file = 'log_app/config.txt'
  target = IO.readlines(file)[0]
  interval = IO.readlines(file)[1]
  url = IO.readlines(file)[2] 
  items_st = IO.readlines(file)[3]
  items = items_st.split(",")
  items2 = []
  items.each do |item|
        items2 = items2 + [item.strip]
  end
  return target.strip, items2, (interval.strip).to_i, url.strip

end

#prepare to send data

# generate a log file  
def generate_log_app()

  #target name, items to be put in the file, and interval to append new items
  target, items, interval, url = load_vars()
  #starts the telemetry in the target
  cmd("#{target} START_TLM")

  #list of telemetry items to be put in the file
  tlm_item = get_tlm_item_list("#{target}", "TLM")
  
  #string to be written in the file every ts  
  st = ""

  #file name
  time = Time.new
  file_name = "log_app/" + time.strftime('%m')+"_"+ time.strftime('%d') +
	"_" + time.strftime('%Y')+ "_log_" + target +".txt"

  puts file_name
  
  #appends the new information to the log file
  File.open(file_name, 'a') do |file|
    file.puts "--------------------------------------------------------------------"
    file.puts "Target: #{target}\nDate: #{time.strftime('%D')}"
    file.puts "--------------------------------------------------------------------"
    while true    
      #for each telemetry item
      st = ""
      tlm_item.each do |item|
        if (items.include? item[0])
          t = tlm_with_units("#{target} TLM #{item[0]}")
          st = st << "#{item[0]}:#{t} \t"
        end
      end
      st = st << "\n"
      print st
      #TODO: post to webservice
      uri = URI.parse(url)
      request = Net::HTTP::Post.new(uri)
      request.content_type = "application/json"
      request.body = JSON.dump({
        "data" => st
      })

      response = Net::HTTP.start(uri.hostname, uri.port, use_ssl: uri.scheme == "https") do |http|
        http.request(request)
      end
      print response
      # write on log
      file.puts st
     # sleep(interval*1)
    end   
  end 
end


print load_vars()
generate_log_app()