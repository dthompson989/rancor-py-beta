class FirstClass:
    instances = 0

    def __init__(self, field1, field2, field3):
        self.__field1 = field1
        self.__field2 = field2
        self.__field3 = field3
        FirstClass.instances += 1

    def get_fields(self):
        return {'field1': self.__field1, 'field2': self.__field2, 'field3': self.__field3}

    def print_fields(self):
        print("Field1:", self.__field1)
        print("Field2:", self.__field2)
        print("Field3:", self.__field3)


class SecondClass(FirstClass):
    def __init__(self, field1, field2, field3, field4):
        super().__init__(field1, field2, field3)
        self.__field4 = field4

    def get_field(self):
        return self.__field4
