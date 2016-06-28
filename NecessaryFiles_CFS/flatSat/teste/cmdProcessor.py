#Telemetry processing for the flat sat project
#based on Telemetry tools bt cFE GSFC

import sys
import getopt

from PyQt4 import QtNetwork
from struct import *

class TlmProcessing():

    pktCount = 0

    def __init__(self, parent=None):
        
        self.udpSocket = QtNetwork.QUdpSocket()
        self.udpSocket.bind(int(udpPort))
        self.udpSocket.readyRead.connect(self.processPendingDatagrams)

    def processPendingDatagrams(self):
        while self.udpSocket.hasPendingDatagrams():
            datagram, host, port = self.udpSocket.readDatagram(self.udpSocket.pendingDatagramSize())
            self.pktCount += 1

            # Packet Header
            #   uint16  StreamId;   0   
            #   uint16  Sequence;   2
            #   uint16  Length;     4 
            # PktSequence = unpack("<H",datagram[2:4])
            #self.ui.sequenceCount.setText(str(self.pktCount))

            #
            # Not accounting for endian right now!
            #
            appName = "".join(unpack("<20s",datagram[12:32]))
            eventText = "".join(unpack("<122sxx",datagram[44:]))
            appName = appName.split("\0")[0]
            eventText = eventText.split("\0")[0]
            eventString = "EVENT ---> "+ appName + " : " + eventText
            #self.ui.eventOutput.append(eventString)
            print eventString

#
# Display usage
#
def usage():
    print "Must specify --title=<page name> --port=<udp_port> --appid=<packet_app_id(hex)> --endian=<endian(L|B) --file=<tlm_def_file>"
    print "     example: --title=Executive Services --port=10800 --appid=800 --file=cfe-es-hk-table.txt --endian=L"
    print "            (quotes are not on the title string in this example)"

 
if __name__ == '__main__':


    #
    # Set defaults for the arguments
    #
    pageTitle = "Event Messages"
    udpPort  = 10000
    appId = 999
    tlmDefFile = "not-needed.txt"
    endian = "L"

    #
    # process cmd line args 
    #
    try:
        opts, args = getopt.getopt(sys.argv[1:], "htpafl", ["help", "title=", "port=", "appid=","file=", "endian="])
    except getopt.GetoptError:
        usage()
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
            sys.exit()
        elif opt in ("-p", "--port"):
            udpPort = arg
        elif opt in ("-t", "--title"):
            pageTitle = arg
        elif opt in ("-f", "--file"):
            tlmDefFile = arg
        elif opt in ("-t", "--appid"):
            appId = arg
        elif opt in ("-e", "--endian"):
            endian = arg

    if endian == 'L':
       py_endian = '<'
    else:
       py_endian = '>'

    #
    # Init the QT application and the Event Message class
    #
    #app = QtGui.QApplication(sys.argv)
    #Telem = TlmProcessing()
    TlmProcessing()

    #Telem.show()
    #sys.exit(app.exec_())
