from pktcomm.packets import PacketComm
import serial
import time

class LoopBack(PacketComm):
    """ For Debugging Packet interface"""

    def __init__(self, timeout=1, pkt_class=None, addr=0x1, eol=None):

        self.eol = '\n'.encode('utf-8') if eol == None else eol.encode('utf-8')
        self.timeout = timeout
        self.addr = addr
        self.rx_buffer = b''
        self.tx_buffer = b''
        self.flush()

        if (pkt_class != None):
            super(LoopBackComm, self).__init__(pkt_class, addr=addr)
        
    def flush(self, resetTXbuffer = True):
        self.rx_buffer = b''
        if (resetTXbuffer):
            self.rx_buffer = b''

    def write(self, dataBytes):
        self.tx_buffer = dataBytes
        self.rx_buffer += dataBytes

    def read(self, nbytes = None):

        if nbytes == None:
            nbytes = self.rx_buffer.index(self.eol)

        if len(self.rx_buffer) >= nbytes:
            ret = self.rx_buffer[:nbytes]
            self.rx_buffer = self.rx_buffer[nbytes:]
            return ret

        else:
            raise RuntimeError('Loopback interface timed out attempting to read {} bytes. Recieved: {}'.format(self.timeout, nbytes, self.rx_buffer))
