#----------------------------------------------------------------------
#------------------------------------------------------------
# Project: CFS+Cosmos
# Author: Rebeca Rodrigues
# Date: 07/2016
# Contact: rebeca.n.rod@gmail.com
# Function: Convert timestamp to datetime format.
#----------------------------------------------------------------------
#------------------------------------------------------------

require 'cosmos/conversions/conversion'
require 'date'
module Cosmos
	class ConvertTimestamp  < Conversion
		def call(value, packet, buffer)
			return Time.at(value)
		end
	end
end
