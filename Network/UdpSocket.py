import socket

from decimal import Decimal
from .packet import Packet
from .packetTypes import PacketType

class UdpSocket:

    def __create__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM);
    
    def __close__(self):
        self.sock.close()
        
    def __init__(self):
        self.__create__()
        
    def __del__(self):
        self.__close__()
    
    def get_local_port(self) -> int:
        return self.sock.getsockname()[1]
        
    def bind(self, port):
        """
            Bind the socket to a specific port
            
            @param: port    Port to bind the socket to
        """
        self.sock.bind( ('localhost', port) )
        
    def send(self, data, server_ip, server_port):
        """
            Send data to a remote peer
            @param: data          Data or Packet to send
            @param: remoteAddress Address of the receiver
            @param: remotePort    Port of the receiver to send the data to
        """

        if data.__class__.__name__ == 'Packet':
            sent = self.sock.sendto(data.raw_data(), (server_ip, server_port))
        else:
            raise Exception("Data type must be 'Packet'.")
            
        if sent < 0:
            raise Exception('Failed to send data');
        
    def receive(self, timeout=0):
        """
            Receive data from a remote peer
           
            This function will WAIT UNTIL the whole packet
            has been received.
           
            @return: (data, remote_address)
        """
        if timeout != 0:
            self.sock.settimeout(timeout)

        try:
            data, server = self.sock.recvfrom(4096)
        except socket.timeout as e:
            print('Connection Timeout')
            raise e

        return data, server
        
if __name__ == "__main__":   
    
    sock = UdpSocket()
    
    packet = Packet(packet_type=PacketType.MESSAGE)
    packet.add("ping")
    sock.send(packet, "127.0.0.1", 5555)

    packet = Packet(packet_type=PacketType.LOGIN)
    packet.add("User_123")
    packet.add("Password_123")
    sock.send(packet, "127.0.0.1", 5555)
    
    data, server = sock.receive()
    packet = Packet(raw_data = data)
    packet.get_type()
    result = packet.get()
    if result == 1:
        print("Login Success")
    else:
        print("Login Failed")
        









