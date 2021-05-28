# pip install sqlite3
import sqlite3


class ConnectionMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Connection(metaclass=ConnectionMeta):
    cnx = None

    def __init__(self):
        self.cnx = sqlite3.connect('database.db',
                                   isolation_level=None)  # autocommit
        self.cnx.cursor().execute("PRAGMA foreign_keys = 1")  # Włączenie sprawdzania kluczy obcych
        # cursor().execute('')

    def getInstance(self):
        return self.cnx.cursor()

    def __del__(self):
        self.cnx.close()


# Example

def create_db():
    cursor = Connection().getInstance()

    querries = [
        """DROP TABLE IF EXISTS `users_currency`;""",
        """DROP TABLE IF EXISTS `users_attribute`;""",
        """DROP TABLE IF EXISTS `users_item`;""",
        """DROP TABLE IF EXISTS `user`;""",
        """
        CREATE TABLE `user` (
            `id`                INTEGER PRIMARY KEY AUTOINCREMENT,
            `username`          VARCHAR(32) NOT NULL UNIQUE,
            `password`          VARCHAR(60) NOT NULL,
            `email`             VARCHAR(255) NOT NULL UNIQUE
        );
        """,
        """
        CREATE TABLE `users_currency` (
            `users_currency_id` INTEGER PRIMARY KEY AUTOINCREMENT,
            `user_id`          INTEGER NOT NULL UNIQUE,
            `gold`              VARCHAR DEFAULT 0 NOT NULL,
            `might`             VARCHAR DEFAULT 1 NOT NULL,
            `cunning`           VARCHAR DEFAULT 1 NOT NULL,
            `psyche`            VARCHAR DEFAULT 1 NOT NULL,
            `lore`              VARCHAR DEFAULT 1 NOT NULL,
            `treasures`         VARCHAR DEFAULT 1 NOT NULL,
            `riches`            VARCHAR DEFAULT 1 NOT NULL,
            FOREIGN KEY(`user_id`) REFERENCES user(`id`)
        );
        """,
        """
        CREATE TABLE `users_attribute` (
            `users_attribute_id` INTEGER PRIMARY KEY AUTOINCREMENT,
            `user_id`          INTEGER NOT NULL UNIQUE,
            `stamina`           VARCHAR DEFAULT 1 NOT NULL,
            `health`            VARCHAR DEFAULT 1 NOT NULL,
            `ploy`              VARCHAR DEFAULT 1 NOT NULL,
            `spirit`            VARCHAR DEFAULT 1 NOT NULL,
            `clarity`           VARCHAR DEFAULT 1 NOT NULL,
            FOREIGN KEY(`user_id`) REFERENCES user(`id`)
        );
        """,
        """
        CREATE TABLE `users_item` (
            `users_item`        INTEGER PRIMARY KEY AUTOINCREMENT,
            `user_id`          INTEGER NOT NULL UNIQUE,
            `item_id`           INTEGER NOT NULL,
            FOREIGN KEY(`user_id`) REFERENCES user(`id`)
        );
        """
    ]

    i = 0
    for querry in querries:
        try:
            cursor.execute(querry)
        except Exception as e:
            print(i, "failed.")
            print(querry)
            raise e

        print(i, "success.")
        i = i + 1


def insert_example_data():
    cursor = Connection().getInstance()

    querry = "INSERT INTO `user` (`username`, `password`, `email`) VALUES (?, ?, ?)"
    values = ("User_123", "$2b$12$ud1WZ0Q/nIh6mkdwwJUgReUXsCMPBR8Wf00gmLmYw4d2EhhyyT75W", "Email_123")  # password: aaaa
    cursor.execute(querry, values)

    querry = "INSERT INTO `user` (`username`, `password`, `email`) VALUES (?, ?, ?)"
    values = ("User_124", "$2b$12$ud1WZ0Q/nIh6mkdwwJUgReUXsCMPBR8Wf00gmLmYw4d2EhhyyT75W", "Email_124")  # password: aaaa
    cursor.execute(querry, values)

    querry = "INSERT INTO `user` (`username`, `password`, `email`) VALUES (?, ?, ?)"
    values = ("User_125", "$2b$12$ud1WZ0Q/nIh6mkdwwJUgReUXsCMPBR8Wf00gmLmYw4d2EhhyyT75W", "Email_125")  # password: aaaa
    cursor.execute(querry, values)

    querry = "INSERT INTO `users_currency` (`user_id`) VALUES (1)"
    cursor.execute(querry)

    querry = "INSERT INTO `users_attribute` (`user_id`) VALUES (1)"
    cursor.execute(querry)


def decimal_test():
    # todo zaokrąglamy decimal do ilus miejsc po przecinku czy ładujemy do bazy ile wlezie?
    # ja bym nie zaokraglal nic
    cursor = Connection().getInstance()
    cursor.execute("""DROP TABLE IF EXISTS `decimaltest`;""")

    querry = """
    CREATE TABLE `decimaltest` (
        `id`        INTEGER PRIMARY KEY AUTOINCREMENT,
        `txt`          TEXT
    );
    """
    i = decimal_test
    try:
        cursor.execute(querry)
    except Exception as e:
        print(i, "failed.")
        print(querry)
        raise e

    print(i, "success.")

    from decimal import getcontext, Decimal
    # x = Decimal('1234567890123456797342394242394372340.1234567890123456901234567890123456890123123')
    x = Decimal('1234567890123456797342394242394372340.1234567890123456901234567890123456890123123'
                '1234567890123456901234567890123456890123123'
                '1234567890123456901234567890123456890123123'
                '1234567890123456901234567890123456890123123'
                '1234567890123456901234567890123456890123123'
                '1234567890123456901234567890123456890123123'
                '1234567890123456901234567890123456890123123'
                '1234567890123456901234567890123456890123123'
                '1234567890123456901234567890123456890123123'
                '1234567890123456901234567890123456890123123'
                '1234567890123456901234567890123456890123123'
                '1234567890123456901234567890123456890123123'
                '1234567890123456901234567890123456890123123'
                '1234567890123456901234567890123456890123123'
                '1234567890123456901234567890123456890123123'
                '1234567890123456901234567890123456890123123'
                '1234567890123456901234567890123456890123123'
                )

    querry = "INSERT INTO `decimaltest` (`txt`) VALUES (?)"
    values = (str(x),)
    cursor.execute(querry, values)

    querry = "SELECT * FROM `decimaltest`"
    cursor.execute(querry)
    for row in cursor:
        print(row)
        print(row[1])
        y = Decimal(row[1])
        if x == y:
            print("decimal dziala")


if __name__ == "__main__":

    #create_db()
    #insert_example_data()
    cursor = Connection().getInstance()

    querry = "SELECT * FROM `user`"
    cursor.execute(querry)
    for row in cursor:
        print(row)

    exit()
    querry = "SELECT * FROM `users_currency`"
    cursor.execute(querry)
    for row in cursor:
        print(row)

    querry = "SELECT * FROM `users_attribute`"
    cursor.execute(querry)
    for row in cursor:
        print(row)

    decimal_test()
