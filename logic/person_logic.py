from core.pyba_logic import PybaLogic


class PersonLogic(PybaLogic):
    def __init__(self):
        super().__init__()

    def getAllPersons(self):
        database = self.createDatabaseObj()
        sql = "select * from person;"
        result = database.executeQuery(sql)
        return result
