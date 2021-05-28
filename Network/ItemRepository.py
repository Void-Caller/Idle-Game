from .AbstractRepository import AbstractRepository

class Item:
    def __init__(self):
        self.id             = None
        self.name           = None
        self.type           = None
        self.req_might      = None
        self.req_cunning    = None
        self.req_psyche     = None
        self.req_lore       = None
        self.might          = None
        self.cunning        = None
        self.psyche         = None
        self.lore           = None

class ItemRepository(AbstractRepository):

    def __create_objects_from_result(self, results):
        items = []

        if not results:
            return None

        for result in results:
            item = Item()
            item.id             = result[0]
            item.name           = result[1]
            item.type           = result[2]
            item.req_might      = result[3]
            item.req_cunning    = result[4]
            item.req_psyche     = result[5]
            item.req_lore       = result[6]
            item.might          = result[7]
            item.cunning        = result[8]
            item.psyche         = result[9]
            item.lore           = result[10]

            items.append(item)

        return items
        
    def __init__(self, reset=False):
        self.name = "item"
        self.delete_querry = """DROP TABLE IF EXISTS `{}`;""".format(self.name)
        self.create_querry = """
        CREATE TABLE `{}` (
            `id` INTEGER PRIMARY KEY AUTOINCREMENT,
            `name`                  VARCHAR NOT NULL,
            `type`                  VARCHAR NOT NULL,
            `req_might`             VARCHAR NOT NULL,
            `req_cunning`           VARCHAR NOT NULL,
            `req_psyche`            VARCHAR NOT NULL,
            `req_lore`              VARCHAR NOT NULL,
            `might`                 VARCHAR NOT NULL,
            `cunning`               VARCHAR NOT NULL,
            `psyche`                VARCHAR NOT NULL,
            `lore`                  VARCHAR NOT NULL
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
        if object.__class__.__name__ == "Item":
            self._add(object)
        else:
            raise TypeError

if __name__ == "__main__":

    itemRepository = ItemRepository()

    item = Item()
    item.name           = "Dziadek do orzechow"
    item.type           = "Weapon"
    item.req_might      = 1
    item.req_cunning    = 2
    item.req_psyche     = 1
    item.req_lore       = 1
    item.might          = 1
    item.cunning        = 2
    item.psyche         = 1
    item.lore           = 1
    #itemRepository.add(item)
    
    item = Item()
    item.name           = "Durszlak Spaczenia"
    item.type           = "Helmet"
    item.req_might      = 11
    item.req_cunning    = 112
    item.req_psyche     = 23
    item.req_lore       = 4
    item.might          = 5
    item.cunning        = 13
    item.psyche         = 8
    item.lore           = 0
    #itemRepository.add(item)

    for item in itemRepository.findAll():
        print (item.id, item.name, item.type,
               item.req_might, item.req_cunning, item.req_psyche, item.req_lore,
               item.might, item.cunning, item.psyche, item.lore)

    item = itemRepository.findOneBy({"id" : 1})
    print (item.id, item.name, item.type,
            item.req_might, item.req_cunning, item.req_psyche, item.req_lore,
            item.might, item.cunning, item.psyche, item.lore)