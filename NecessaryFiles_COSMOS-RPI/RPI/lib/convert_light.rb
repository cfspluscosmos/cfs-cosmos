require 'cosmos/conversions/conversion'
module Cosmos
	class ConvertLight  < Conversion
		def call(value, packet, buffer)
			return (value.to_f*100)/1023
		end
	end
end
