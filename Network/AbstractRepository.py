
from .database import Connection

class AbstractRepository:
    def __init__(self, reset):
        self.cursor = Connection().getInstance()
        if reset:
            try:
                self.cursor.execute(self.delete_querry)
            except Exception as e:
                print(self.delete_querry)
                print("Drop failed.")
                print(e)
                raise e

            try:
                self.cursor.execute(self.create_querry)
            except Exception as e:
                print(self.create_querry)
                print("Create failed.")
                print(e)
                raise e

    def _findAll(self):
        
        self.get_all_querry = """
            SELECT * FROM {};
        """.format(self.name)


        try:
            self.cursor.execute(self.get_all_querry)
        except Exception as e:
            print(self.get_all_querry)
            print ("failed.")
            print(e)
            return None
        
        result = self.cursor.fetchall()
        return result

    def _findBy(self, arr):
        if arr == {}:
            return self.getAll()

        keys = list(arr.keys())

        self.querry = """
            SELECT * FROM {}
            WHERE `{}` = "{}"
        """.format(self.name, keys[0], arr[keys[0]])

        for i in range(1, len(arr) ):
            self.querry = (self.querry + " AND `{}` = \"{}\"").format(keys[i], arr[keys[i]])
        
        try:
            #print ("DEBUG:", self.querry)
            self.cursor.execute(self.querry)
        except Exception as e:
            print(self.querry)
            print ("failed.")
            print(e)
            return None
        
        result = self.cursor.fetchall()
        return result

    def _add(self, object):
        arr = object.__dict__
        keys = list(arr.keys())
        values = list(arr.values())

        new_keys = []
        new_values = []

        for i in range(len(arr)):
            if arr[keys[i]] not in ['', None]:
                new_keys.append(keys[i])
                new_values.append(arr[keys[i]])

        id_arr = { key:value for (key,value) in arr.items() if key.find("id") != -1 and value != None }

        #exist = self._findBy( arr )
        exist = self._findBy({new_keys[i]: new_values[i] for i in range(len(new_values))})

        if id_arr == {} or exist == []:
            self.querry = "INSERT INTO `{}` (`{}`" + ((", `{}`")*(len(new_keys)-1)) + ")"
            self.querry = self.querry.format(self.name, *new_keys)

            self.querry = self.querry + " VALUES (\"{}\"" + ((", \"{}\"")*(len(new_keys)-1)) + ")"
            self.querry = self.querry.format(*new_values)
        else:
            values = []
            values_id = []
            arr_len = 0
            for k, v in arr.items():
                if v == None:
                    continue
                values.append(k)
                values.append(v)
                arr_len = arr_len + 1

            for k, v in id_arr.items():
                if v == None:
                    continue
                values_id.append(k)
                values_id.append(v)

            self.querry = "UPDATE {} SET ".format(self.name)
            self.querry = self.querry + ("`{}`={}" + ", `{}`={}"* (arr_len-1)).format(*values)

            self.querry = self.querry + (" WHERE `{}`={}" + " AND `{}`={}" * (len(id_arr)-1))
            self.querry = self.querry.format( *values_id )

        try:
            #print ("DEBUG:", self.querry)
            self.cursor.execute(self.querry)
        except Exception as e:
            print(self.querry)
            print ("failed.")
            print(e)
            return False

        query = "SELECT last_insert_rowid()"
        self.cursor.execute(query)
        result = self.cursor.fetchall()

        return result[0][0]

    def _execute(self, query):
        self.cursor = Connection().getInstance()
        try:
            self.cursor.execute(query)
        except Exception as e:
            print(query)
            print("failed. ->", e)
            return None
        return self.cursor.fetchall()

if __name__ == "__main__":
    ar = AbstractRepository()
    ar.name = "users"
    print ( ar.findBy( {"users_id" : "1"} ) )