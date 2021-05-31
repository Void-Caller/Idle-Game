import threading
import time
import bcrypt

from decimal import Decimal

from .UdpSocket import UdpSocket
from .database import Connection
from .packet import Packet
from .packetTypes import PacketType
from .UserRepository import UserRepository, User
from .UserCurrencyRepository import UserCurrencyRepository, UserCurrency
from .ItemRepository import ItemRepository, Item
from .UserEquipmentRepository import UserEquipmentRepository, UserEquipment


class PacketHandler:

    def __init__(self, server, cursor):
        self.cursor = cursor
        self.server = server
        self.userEquipmentRepository = UserEquipmentRepository()
        self.userCurrencyRepository = UserCurrencyRepository()
        self.itemRepository = ItemRepository()
        self.userRepository = UserRepository()

    def handle(self, packet, client_ip, client_port):
        type = packet.get_type()

        print("DEBUG: Type ->", type)
        outgoing_packet = Packet()

        if type == PacketType.MESSAGE:
            print("message: ", packet.get())

        elif type == PacketType.PING:
            outgoing_packet = Packet(PacketType.PING)
            outgoing_packet.add("pong")

        elif type == PacketType.LOGIN:
            outgoing_packet = Packet(PacketType.LOGIN)

            login = packet.get()
            password = packet.get()
            print("DEBUG: Login ->", login)
            print("DEBUG: Password ->", password)

            user = self.userRepository.findOneBy({"username": login})

            if user is not None:
                print("DEBUG: received: ", login.encode())
                print("DEBUG: received: ", password.encode())
                print("DEBUG: Hashed Password ->", bcrypt.checkpw(password.encode(), user.password.encode()) )
                print("DEBUG: cmp ->", user.password)

                if bcrypt.checkpw(password.encode(), user.password.encode()):
                    user_data = [user, client_ip, client_port]
                    if user_data not in self.server.users:
                        print("DEBUG: Login Success.")
                        outgoing_packet.add(1)
                        self.server.users.append([user, client_ip, client_port])
                        print(self.server.users)
                        return outgoing_packet
                    else:
                        self.server.users.remove(user_data)

            print("DEBUG: Login Failed.")
            outgoing_packet.add(0)

        elif type == PacketType.LOGOUT:
            outgoing_packet = Packet(PacketType.LOGOUT)
            user = self.server.get_user(client_ip, client_port)
            if user != None:
                self.server.users.remove(user)
                outgoing_packet.add(1)

            outgoing_packet.add(0)

        elif type == PacketType.REGISTER:
            outgoing_packet = Packet(PacketType.REGISTER)
            login = packet.get()
            password = packet.get()
            email = packet.get()

            salt = bcrypt.gensalt()
            hashed_password = bcrypt.hashpw(password.encode(), salt)
            print("DEBUG: Hashed Password ->", hashed_password)

            user = User()
            user.username = login
            user.password = hashed_password.decode()
            user.email = email

            result_login = self.userRepository.findByName(login)
            result_email = self.userRepository.findByEmail(email)

            if result_login:
                outgoing_packet.add(2)
                return outgoing_packet;

            if result_email:
                outgoing_packet.add(3)
                return outgoing_packet

            user_id = self.userRepository.add(user)
            print(user)

            userCurrency = UserCurrency()
            userCurrency.user_id = user_id
            self.userCurrencyRepository.add(userCurrency)

            outgoing_packet.add(1)
            return outgoing_packet

        elif type == PacketType.GET_STATS:
            outgoing_packet = Packet(PacketType.GET_STATS)
            user = self.server.get_user(client_ip, client_port)
            if (user == None):
                return outgoing_packet

            userCurrency = self.userCurrencyRepository.findOneBy({"user_id": user[0].id})
            outgoing_packet.add(Decimal(userCurrency.gold))
            outgoing_packet.add(Decimal(userCurrency.treasure))
            outgoing_packet.add(Decimal(userCurrency.might))
            outgoing_packet.add(Decimal(userCurrency.cunning))
            outgoing_packet.add(Decimal(userCurrency.psyche))
            outgoing_packet.add(Decimal(userCurrency.lore))
            outgoing_packet.add(Decimal(userCurrency.stamina))
            outgoing_packet.add(Decimal(userCurrency.health))
            outgoing_packet.add(Decimal(userCurrency.ploy))
            outgoing_packet.add(Decimal(userCurrency.spirit))
            outgoing_packet.add(Decimal(userCurrency.clarity))

            return outgoing_packet

        elif type == PacketType.GET_ITEMS:
            outgoing_packet = Packet(PacketType.GET_ITEMS)
            user = self.server.get_user(client_ip, client_port)
            if (user == None):
                return outgoing_packet

            userEquipment = self.userEquipmentRepository.findBy({"user_id": user[0].id})
            if userEquipment == None:
                outgoing_packet.add(0)
                return outgoing_packet

            outgoing_packet.add(int(len(userEquipment)))

            for item in userEquipment:
                outgoing_packet.add(int(item.item_id))
                outgoing_packet.add(item.equipped)

            return outgoing_packet

        elif type == PacketType.GET_ITEM_INFO:
            outgoing_packet = Packet(PacketType.GET_ITEM_INFO)
            item_id = packet.get()

            item = self.itemRepository.findOneBy({"id": item_id})
            if item == None:
                return outgoing_packet

            outgoing_packet.add(item.name)
            outgoing_packet.add(item.type)
            outgoing_packet.add(Decimal(item.req_might))
            outgoing_packet.add(Decimal(item.req_cunning))
            outgoing_packet.add(Decimal(item.req_psyche))
            outgoing_packet.add(Decimal(item.req_lore))
            outgoing_packet.add(Decimal(item.might))
            outgoing_packet.add(Decimal(item.cunning))
            outgoing_packet.add(Decimal(item.psyche))
            outgoing_packet.add(Decimal(item.lore))
            print("itemlore", item.lore)

            return outgoing_packet

        elif type == PacketType.SAVE_STATS:
            outgoing_packet = Packet(PacketType.SAVE_STATS)
            user = self.server.get_user(client_ip, client_port)
            if (user == None):
                outgoing_packet.add(0)
                return outgoing_packet

            userCurrency = UserCurrency()
            userCurrency.user_id = user[0].id
            userCurrency.might = str(packet.get())
            userCurrency.cunning = str(packet.get())
            userCurrency.psyche = str(packet.get())
            userCurrency.lore = str(packet.get())
            userCurrency.gold = str(packet.get())
            userCurrency.treasure = str(packet.get())
            userCurrency.stamina = str(packet.get())
            userCurrency.health = str(packet.get())
            userCurrency.ploy = str(packet.get())
            userCurrency.spirit = str(packet.get())
            userCurrency.clarity = str(packet.get())

            if self.userCurrencyRepository.add(userCurrency):
                outgoing_packet.add(1)
            else:
                outgoing_packet.add(0)

            return outgoing_packet

        elif type == PacketType.SAVE_ITEMS:
            outgoing_packet = Packet(PacketType.SAVE_ITEMS)
            user = self.server.get_user(client_ip, client_port)
            if (user == None):
                return outgoing_packet

            n = packet.get()

            if self.userEquipmentRepository.delete_old_items(user[0].id):  # TODO
                outgoing_packet.add(0)
                return outgoing_packet

            for i in range(n):
                userEquipment = UserEquipment()
                userEquipment.item_id = int(packet.get())
                userEquipment.user_id = user[0].id
                userEquipment.equipped = int(packet.get())

                if not self.userEquipmentRepository.add(userEquipment):
                    outgoing_packet.add(0)
                    return outgoing_packet

            outgoing_packet.add(1)
            return outgoing_packet

        return outgoing_packet


class Server:

    def __listen(self):
        print("Listening...")
        cursor = Connection().getInstance()
        packet_handler = PacketHandler(self, cursor)

        while True:
            data, client_info = self.incoming.receive()
            client_ip, client_port = client_info

            print("DEBUG: Received from " + client_ip + ":" + str(client_port))
            print("DEBUG: data: [", data, "]", sep='')

            packet = Packet(raw_data=data)
            outgoing_packet = packet_handler.handle(packet, client_ip, client_port)
            if not outgoing_packet.get_size() == 0:
                self.outgoing.send(outgoing_packet, client_ip, client_port)

    def __init__(self):
        self.incoming = UdpSocket()
        self.incoming.bind(5555)
        self.users = []  # [ User, ip, port ]

        self.outgoing = UdpSocket()
        self.outgoing.bind(5556)

        self.listening_thread = threading.Thread(target=self.__listen, args=(), daemon=True)

    def run(self):
        self.running = True
        self.listening_thread.start()
        while (True):
            time.sleep(1.0)

    def get_user(self, ip, port):
        for user in self.users:
            if user[1] == ip and user[2] == port:
                return user
        return None

if __name__ == "__main__":
    s = Server()
    s.run()
