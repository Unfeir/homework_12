from collections import UserDict
from datetime import date
from pickle import dump, load
import re

class AddressBook(UserDict): # та ми потім додамо логіку пошуку за записами до цього класу
    
    def __init__(self):
        super().__init__()
        self.pagination = 1
        self.from_index = 0
        self.to_index = 1
        
        
    
    def add_record(self, record):
        self.data[record.name.value] = record
        
#################################################################################################
    def save_contacts(self):
        filename = r"D:\study\GoIT\cours\python_core\module_12\homework_12\save.bin"
        with open(filename, "wb") as file:
            dump(self.data, file)
        
    def load_contacts(self):
        filename = r"D:\study\GoIT\cours\python_core\module_12\homework_12\save.bin"
        try:
            with open(filename, "rb") as file:
                self.data = load(file)
        except FileNotFoundError:
            return
        
    def search_contacts(self, search_value):
        contacts = []
        for key, val in self.data.items():
            if search_value in key:
                contacts.append(self.data[key])
            else:
                for phone in val.get_phones():
                    if search_value in phone:
                        contacts.append(self.data[key])
        
        return contacts
 #################################################################################################
        
        
    def __next__(self):
        
        
        self.list_data = list(self.data.keys()) #keys
        if self.from_index >= len(self.list_data):
            self.from_index = 0
            self.to_index = self.pagination
        else:
            result = self.list_data[self.from_index:self.to_index]
            self.from_index += self.pagination
            self.to_index += self.pagination
            return result

    def __iter__(self):
        return self
        

class Record:  # який відповідає за логіку додавання/видалення/редагування необов'язкових полів та зберігання обов'язкового поля Name.
    
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None
    
   
    def add_phone(self, phone):
        self.phones.append(Phone(phone))
        
    def change_phone(self, phone, new_value):
        for item in self.phones:
            if item.value == phone:
                item.value = new_value
    
    def days_to_birthday(self):
        if self.birthday:
            sysdate = date.today()
            if self.birthday.value.replace(year=sysdate.year) > sysdate:
                return (self.birthday.value.replace(year=sysdate.year) - sysdate).days
            else:
                return (self.birthday.value.replace(year=sysdate.year + 1) - sysdate).days
        else:
            return None
     
        
    def del_phone(self, phone): # видаляти треба не за екземпляром а за номером з екземпляра            
         for item in self.phones:
            if item.value == phone:
                self.phones.remove(item)

    def get_phones(self):
        all_phones = [phone.value for phone in self.phones]
        return all_phones
    


class Field:  # який буде батьківським для всіх полів, у ньому потім реалізуємо логіку загальну для всіх полів.
    def __init__(self, value):
        self.__value = value
        self.value = value
        
    @property
    def value(self):
        return self.__value
    
    @value.setter
    def value(self, value):
        self.__value = value


class Birthday(Field):
       
    @Field.value.setter
    def value(self, value):
        if re.search(r"\b\d{2}[.]\d{2}[.]\d{4}", value):
            value_splitted = value.split(".")
            self.__value = date(year=int(value_splitted[2]), month=int(
                value_splitted[1]), day=int(value_splitted[0]))
        else:
            raise Exception("Birthday must be in DD.MM.YYYY format")

    def __str__(self) -> str:
        return self.__value.strftime("%d.%m.%Y")

class Name(Field):
    pass

# необов'язкове поле з телефоном та таких один запис (Record) може містити кілька.
class Phone(Field):
   
    @Field.value.setter
    def value(self, value):
        analize = re.search(r"\+380\d{9}\b", value)
        if analize:
            self.__value = analize.group()
        else:
            raise Exception("phone must be in +380CCXXXXXXX format")
