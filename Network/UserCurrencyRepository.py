from .AbstractRepository import AbstractRepository


class UserCurrency:
    def __init__(self):
        self.id = None
        self.user_id = None
        self.gold = 0
        self.treasure = 0
        self.might = 1
        self.cunning = 1
        self.psyche = 1
        self.lore = 1
        self.might_exp = 0
        self.cunning_exp = 0
        self.psyche_exp = 0
        self.lore_exp = 0
        self.stamina = 20
        self.health = 20
        self.ploy = 20
        self.spirit = 20
        self.clarity = 20
        self.stamina_max = 100
        self.health_max = 100
        self.ploy_max = 100
        self.spirit_max = 100
        self.clarity_max = 100
        self.work_level = 1
        self.rest_level = 1


class UserCurrencyRepository(AbstractRepository):

    def __create_objects_from_result(self, results):
        userCurrencies = []

        if not results:
            return None

        for result in results:
            userCurrency = UserCurrency()
            userCurrency.id = result[0]
            userCurrency.user_id = result[1]
            userCurrency.gold = result[2]
            userCurrency.treasure = result[3]
            userCurrency.might = result[4]
            userCurrency.cunning = result[5]
            userCurrency.psyche = result[6]
            userCurrency.lore = result[7]
            userCurrency.might_exp = result[8]
            userCurrency.cunning_exp = result[9]
            userCurrency.psyche_exp = result[10]
            userCurrency.lore_exp = result[11]
            userCurrency.stamina = result[12]
            userCurrency.health = result[13]
            userCurrency.ploy = result[14]
            userCurrency.spirit = result[15]
            userCurrency.clarity = result[16]
            userCurrency.stamina_max = result[17]
            userCurrency.health_max = result[18]
            userCurrency.ploy_max = result[19]
            userCurrency.spirit_max = result[20]
            userCurrency.clarity_max = result[21]
            userCurrency.work_level = result[22]
            userCurrency.rest_level = result[23]

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
            `might_exp`             VARCHAR DEFAULT 0 NOT NULL,
            `cunning_exp`           VARCHAR DEFAULT 0 NOT NULL,
            `psyche_exp`            VARCHAR DEFAULT 0 NOT NULL,
            `lore_exp`              VARCHAR DEFAULT 0 NOT NULL,
            `stamina`               VARCHAR DEFAULT 20 NOT NULL,
            `health`                VARCHAR DEFAULT 20 NOT NULL,
            `ploy`                  VARCHAR DEFAULT 20 NOT NULL,
            `spirit`                VARCHAR DEFAULT 20 NOT NULL,
            `clarity`               VARCHAR DEFAULT 20 NOT NULL,
            `stamina_max`           VARCHAR DEFAULT 100 NOT NULL,
            `health_max`            VARCHAR DEFAULT 100 NOT NULL,
            `ploy_max`              VARCHAR DEFAULT 100 NOT NULL,
            `spirit_max`            VARCHAR DEFAULT 100 NOT NULL,
            `clarity_max`           VARCHAR DEFAULT 100 NOT NULL,
            `work_level`            INT DEFAULT 1 NOT NULL,
            `rest_level`            INT DEFAULT 1 NOT NULL,
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
    userCurrency.user_id = 1

    userCurrencyRepository.add(userCurrency)
    userCurrency.user_id = 2
    userCurrencyRepository.add(userCurrency)
    userCurrency.user_id = 3
    userCurrencyRepository.add(userCurrency)

    for userCurrency in userCurrencyRepository.findAll():
        print(userCurrency.id, userCurrency.user_id, userCurrency.gold, userCurrency.treasure,
              userCurrency.might, userCurrency.cunning, userCurrency.psyche, userCurrency.lore,
              userCurrency.stamina, userCurrency.health, userCurrency.ploy, userCurrency.spirit, userCurrency.clarity)

    userCurrency = userCurrencyRepository.findOneBy({"id": 1})
    print(userCurrency.id, userCurrency.user_id, userCurrency.gold, userCurrency.treasure,
          userCurrency.might, userCurrency.cunning, userCurrency.psyche, userCurrency.lore,
          userCurrency.stamina, userCurrency.health, userCurrency.ploy, userCurrency.spirit, userCurrency.clarity)
