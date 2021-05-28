from decimal import getcontext, Decimal
from .packetTypes import PacketType
import struct

class Packet:
    supported_types = ["Decimal", "int", "float", "str"]
    __data_type = {
        'Decimal'   : 1,
        'int'       : 2,
        'float'     : 3,
        'str'       : 4,
    }
    
    def __init__(self, packet_type = None, raw_data = None):
        self.data = b''; # bytes
        self.unpacket = False;
        
        if not packet_type == None:
            self.data = self.data + struct.pack("!I", packet_type.value)
            return
            
        if not raw_data == None:
            self.data = raw_data
     
    def add(self, data):

        type = data.__class__.__name__
        if not type in self.supported_types:
            raise Exception("Types supported by Packet are only " + str(self.supported_types) )
        
        self.data = self.data + struct.pack("!I", self.__data_type[type])

        if type == 'int':
            bytes = struct.pack("!I", data)
            self.data = self.data + bytes
        elif type == 'float':
            bytes = struct.pack("!f", data)
            self.data = self.data + bytes
        elif type == 'str':
            bytes = data.encode()
            length = struct.pack("!I", len(bytes))
            self.data = self.data + length + bytes
        elif type == 'Decimal':
            bytes = str(data).encode()
            length = struct.pack("!I", len(bytes))
            self.data = self.data + length + bytes
         
    def get_type(self):
        if self.unpacket:
            raise Exception("You can get_type only once,");
        self.unpacket = True
        value = struct.unpack("!I", self.data[0:4])
        self.data = self.data[4:]
        return PacketType(value[0])
    
    def get(self):
        if not self.unpacket:
            raise Exception("Must call once packet.get_type before getting data.");
        try:
            type = struct.unpack("!I", self.data[0:4])
            self.data = self.data[4:]
            type = type[0]
        except:
            print ('No more data.');
            return None
        
        if type == self.__data_type['int']:
            value = struct.unpack("!I", self.data[0:4])
            self.data = self.data[4:]
            return value[0]
            
        if type == self.__data_type['float']:
            value = struct.unpack("!f", self.data[0:4])
            self.data = self.data[4:]
            return value[0]
            
        if type == self.__data_type['str']:
            length = struct.unpack("!I", self.data[0:4])
            self.data = self.data[4:]
            
            bytes = self.data[0:length[0]]
            self.data = self.data[length[0]:]
            return bytes.decode('utf-8')
            
        if type == self.__data_type['Decimal']:
            length = struct.unpack("!I", self.data[0:4])
            self.data = self.data[4:]
            
            bytes = self.data[0:length[0]]
            self.data = self.data[length[0]:]
            return Decimal(bytes.decode('utf-8'))

    def raw_data(self):
        return self.data

    def get_size(self):
        return len(self.data)

if __name__ == "__main__":
    p = Packet(packet_type = PacketType.MESSAGE)
    p.add(55)
    p.add(31)
    p.add(105)
    p.add(105.55)
    p.add("string 123")
    p.add("string z polskimi znakami  \"ą, ć, ę, ł, ń, ó, ś, ź, ż\"")
    p.add(Decimal("111.23213311"))
    p.add(Decimal("113434341.82156852"))

    tt = p.get_type()
    print(tt)
    print( p.get() )
    print( p.get() )
    print( p.get() )
    print( p.get() )
    print( p.get() )
    print( p.get() )
    print( p.get() )
    print( p.get() )


