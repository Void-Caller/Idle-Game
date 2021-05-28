from .AbstractRepository import AbstractRepository

class UserCurrency:
    def __init__(self):
        self.id         = None
        self.user_id    = None
        self.gold       = None
        self.treasure   = None
        self.might      = None
        self.cunning    = None
        self.psyche     = None
        self.lore       = None
        self.stamina    = None
        self.health     = None
        self.ploy       = None
        self.spirit     = None
        self.clarity    = None

class UserCurrencyRepository(AbstractRepository):

    def __create_objects_from_result(self, results):
        userCurrencies = []

        if not results:
            return None

        for result in results:
            userCurrency = UserCurrency()
            userCurrency.id         = result[0]
            userCurrency.user_id    = result[1]
            userCurrency.gold       = result[2]
            userCurrency.treasure   = result[3]
            userCurrency.might      = result[4]
            userCurrency.cunning    = result[5]
            userCurrency.psyche     = result[6]
            userCurrency.lore       = result[7]
            userCurrency.stamina    = result[8]
            userCurrency.health     = result[9]
            userCurrency.ploy       = result[10]
            userCurrency.spirit     = result[11]
            userCurrency.clarity    = result[12]

            userCurrencies.append(userCurrency)

        return userCurrencies
        
    def __init__(self, reset=False):
        self.name = "user_currency"
        self.delete_querry = """DROP TABLE IF EXISTS `{}`;""".format(self.name)
        self.create_querry = """
        CREATE TABLE `{}` (
            `id` INTEGER PRIMARY KEY AUTOINCREMENT,
            `user_id`               INTEGER NOT NULL UNIQUE,
            `gold`                  VARCHAR DEFAULT 0 NOT NULL,
            `treasure`              VARCHAR DEFAULT 0 NOT NULL,
            `might`                 VARCHAR DEFAULT 1 NOT NULL,
            `cunning`               VARCHAR DEFAULT 1 NOT NULL,
            `psyche`                VARCHAR DEFAULT 1 NOT NULL,
            `lore`                  VARCHAR DEFAULT 1 NOT NULL,
            `stamina`               VARCHAR DEFAULT 1 NOT NULL,
            `health`                VARCHAR DEFAULT 1 NOT NULL,
            `ploy`                  VARCHAR DEFAULT 1 NOT NULL,
            `spirit`                VARCHAR DEFAULT 1 NOT NULL,
            `clarity`               VARCHAR DEFAULT 1 NOT NULL,
            FOREIGN KEY(`user_id`)  REFERENCES user(`id`)
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
        if object.__class__.__name__ == "UserCurrency":
            return self._add(object)
        else:
            raise TypeError

if __name__ == "__main__":

    userCurrencyRepository = UserCurrencyRepository(True)

    userCurrency = UserCurrency()
    userCurrency.user_id    = 1
    userCurrency.gold       = 1
    userCurrency.treasure   = 1
    userCurrency.might      = 5
    userCurrency.cunning    = 5
    userCurrency.psyche     = 5
    userCurrency.lore       = 5
    userCurrency.stamina    = 10
    userCurrency.health     = 10
    userCurrency.ploy       = 10
    userCurrency.spirit     = 10
    userCurrency.clarity    = 10

    userCurrencyRepository.add(userCurrency)
    userCurrency.user_id    = 2
    userCurrencyRepository.add(userCurrency)
    userCurrency.user_id    = 3
    userCurrencyRepository.add(userCurrency)

    for userCurrency in userCurrencyRepository.findAll():
        print (userCurrency.id, userCurrency.user_id, userCurrency.gold, userCurrency.treasure,
               userCurrency.might, userCurrency.cunning, userCurrency.psyche, userCurrency.lore,
               userCurrency.stamina, userCurrency.health, userCurrency.ploy, userCurrency.spirit, userCurrency.clarity)

    userCurrency = userCurrencyRepository.findOneBy({"id" : 1})
    print (userCurrency.id, userCurrency.user_id, userCurrency.gold, userCurrency.treasure,
            userCurrency.might, userCurrency.cunning, userCurrency.psyche, userCurrency.lore,
            userCurrency.stamina, userCurrency.health, userCurrency.ploy, userCurrency.spirit, userCurrency.clarity)