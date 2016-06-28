require 'cosmos/conversions/conversion'
module Cosmos
	class ConvertTemp  < Conversion
		def call(value, packet, buffer)
			return ((value.to_f * 330)/1023)-50
		end
	end

end
