from .AbstractRepository import AbstractRepository

class UserEquipment:
    def __init__(self):
        self.id             = None
        self.user_id        = None
        self.item_id        = None
        self.equipped       = None

class UserEquipmentRepository(AbstractRepository):

    def __create_objects_from_result(self, results):
        userEquipments = []

        if not results:
            return None

        for result in results:
            userEquipment = UserEquipment()
            userEquipment.id             = result[0]
            userEquipment.user_id        = result[1]
            userEquipment.item_id        = result[2]
            userEquipment.equipped       = result[3]

            userEquipments.append(userEquipment)

        return userEquipments
        
    def __init__(self, reset=False):
        self.name = "user_equipment"
        self.delete_querry = """DROP TABLE IF EXISTS `{}`;""".format(self.name)
        self.create_querry = """
        CREATE TABLE `{}` (
            `id` INTEGER PRIMARY KEY AUTOINCREMENT,
            `user_id`               INTEGER NOT NULL,
            `item_id`               INTEGER NOT NULL,
            `equipped`              INTEGER NOT NULL,
            FOREIGN KEY(`user_id`)  REFERENCES user(`id`),
            FOREIGN KEY(`item_id`)  REFERENCES item(`id`)
        );
        """.format(self.name)
        super().__init__(reset)

    def findAll(self):
        results = self._findAll()
        return self.__create_objects_from_result(results)

    def findBy(self, arr):
        results = self._findBy(arr)
        return self.__create_objects_from_result(results)

    def findOneBy(self, arr):
        result = self.findBy(arr)
        if not result is None and len(result) > 0:
            return result[0]
        return None

    def add(self, object):
        if object.__class__.__name__ == "UserEquipment":
            return self._add(object)
        else:
            raise TypeError

    def delete_old_items(self, user_id):
        querry = "DELETE FROM {} WHERE `user_id` = {}".format(self.name, user_id)
        try:
            self.cursor.execute(querry)
        except Exception as e:
            print(querry)
            print ("failed.")
            print(e)

    def findByUserId(self, name):
        query = """ SELECT * FROM `{}` WHERE `username` = "qwe" """.format(self.name, name)
        result = self._execute(query)
        return result

if __name__ == "__main__":

    userEquipmentRepository = UserEquipmentRepository(True)

    userEquipment = UserEquipment()
    userEquipment.user_id = 18
    userEquipment.item_id = 1
    userEquipment.equipped = True
    userEquipmentRepository.add(userEquipment)

    userEquipment = UserEquipment()
    userEquipment.user_id = 18
    userEquipment.item_id = 2
    userEquipment.equipped = True
    userEquipmentRepository.add(userEquipment)

    userEquipment = UserEquipment()
    userEquipment.user_id = 18
    userEquipment.item_id = 2
    userEquipment.equipped = False
    userEquipmentRepository.add(userEquipment)
    
    userEquipment = UserEquipment()
    userEquipment.user_id = 18
    userEquipment.item_id = 2
    userEquipment.equipped = False
    userEquipmentRepository.add(userEquipment)

    userEquipmentRepository.delete_old_items(1)

    for item in userEquipmentRepository.findAll():
        print (item.id, item.user_id, item.item_id, item.equipped)
