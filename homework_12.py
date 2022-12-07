from entitys import AddressBook, Record, Name, Phone, Birthday
from re import search

address_book = AddressBook()


def input_error(func):
    """Всі помилки введення користувача повинні оброблятися за допомогою декоратора input_error. 
       Цей декоратор відповідає за повернення користувачеві повідомлень виду:
       "Enter user name", "Give me name and phone please" і т.п. 
       Декоратор input_error обробляє вийнятки
       що виникають у функціях-handler (KeyError, ValueError, IndexError) та повертати відповідну відповідь користувачеві."""

    def wraper(*args):

        try:
            result = func(*args)
        except KeyError:
            return "Enter user name"
        except ValueError as err:
            return err  # "Wrong phone number"
        except IndexError:
            return "Give me name and phone please"
        # except StopIteration:
        #     return "no more contact"
        except Exception as err:
            return err
        else:
            return result

    return wraper


def parser(text):
    if text:
        normalise_text = text.replace(
            "good bye", "good_bye").replace("show all", "show_all")
        # формуємо кортеж із назви функції і аргументів для неї
        return normalise_text.split()[0], normalise_text.split()[1:]


@input_error
def hello(*args):
    """ відповідає у консоль "How can I help you?"""
    return "How can I help you?"


@input_error
def good_bye(*args):
    ''' "good bye", "close", "exit" по будь-якій з цих команд бот завершує свою роботу після того, як виведе у консоль "Good bye!".'''
    return "Good bye!"


@input_error
def add_func(args):
    """За цією командою бот зберігає у пам'яті (у словнику наприклад) новий контакт. 
    При наявності контакту з таким іменем дописує телефон/телефони до переліку існуючих, ігнруючи дублі
    Замість ... користувач вводить ім'я та номер телефону, обов'язково через пробіл."""

    name = args[0].capitalize()
    phones = args[1:]
    birthday = None

    for item in phones:
        bd = search(r"\b\d{2}[.]\d{2}[.]\d{4}", item)
        if bd:
            birthday = bd.group()
            phones.remove(birthday)

    if name in address_book.data.keys():
        for phone in phones:
            if phone not in address_book[name].get_phones():
                address_book[name].add_phone(phone)

        if birthday:
            address_book[name].birthday = Birthday(birthday)
            return f"phones:[{', '.join(phones)}] and [{birthday}] as BD was added to {name}"

        return f"{', '.join(phones)} was added to {name}"
    else:
        address_book.add_record(Record(name))
        if phones:
            for phone in phones:
                if phone not in address_book[name].get_phones():
                    address_book[name].add_phone(phone)
        if birthday:
            address_book[name].birthday = Birthday(birthday)

        return f"{name} was added with phone:[{', '.join(phones)}] and BD: [{birthday}]"


@input_error
def change_func(args):
    """За цією командою бот зберігає в пам'яті новий номер телефону існуючого контакту. 
    Замість ... користувач вводить ім'я та номер телефону, обов'язково через пробіл."""
    name = args[0].capitalize()
    phone = int(args[1])
    new_phone = int(args[2])
    address_book[name].change_phone(phone, new_phone)
    return f"{name}`s phone was changed from {phone} to {new_phone}"


@input_error
def phone_func(args):
    """За цією командою бот виводить у консоль номер телефону для зазначеного контакту. 
    Замість ... користувач вводить ім'я контакту, чий номер треба показати."""
    name = args[0].capitalize()
    all_phones = list(map(lambda x: str(x), address_book[name].get_phones()))
    return f"{name}`s phone number is {', '.join(all_phones)}"


@input_error
def dell_func(args):
    """За цією командою бот видаляє номер телефону для зазначеного контакту. 
    Замість ... користувач вводить ім'я контакту, чий номер треба показати."""
    name = args[0].capitalize()
    phone = int(args[1])
    if phone in address_book[name].get_phones():
        address_book[name].del_phone(phone)
        return f"{name}`s phone number '{phone}' was delleted"
    else:
        return f"{name} have no such number:'{phone}' "


@input_error
def pagination(args):
    """За цією командою бот виводить вказану кількість записів."""

    if args:
        address_book.to_index = address_book.from_index + int(args[0])
        address_book.pagination = int(args[0])

    contacts = next(address_book)
    if contacts:
        page = ""
        for item in contacts:
            page += f"{item} - Phones [{address_book[item].get_phones()}], BD:[{address_book[item].birthday}]\n"
        return page
    else:
        return "you reach the end of list. Start again?"


@input_error
def show_all_func(*args):
    """За цією командою бот виводить всі збереженні контакти з номерами телефонів у консоль."""
    contacts = ""

    for k in address_book.data:

        contacts += f"{k} - Phones [{address_book[k].get_phones()}], BD:[{address_book[k].birthday}]\n"

    return contacts


@input_error
def show_birthday(args):
    """За цією командою бот виводить повертає кількість днів до наступного дня народження."""
    name = args[0].capitalize()

    if address_book[name].birthday:
        return f"{name}`s birthday is {address_book[name].birthday} it`s {address_book[name].days_to_birthday()} days before the birthday "
    else:
        return "There is no information"
    
#################################################################################################    
@input_error
def save_contacts(*args):
    address_book.save_contacts()
    return "Contacts was saved"


@input_error
def load_contacts(*args):
    address_book.load_contacts()
    return "Contacts was loaded"


@input_error
def search_contacts(args):
    result = ""
    contacts = address_book.search_contacts(*args)
    if contacts:
        for contact in contacts:
            name = contact.name.value
            all_phones = list(map(lambda x: str(x), contact.get_phones()))
            result += f"{name} with {', '.join(all_phones)}\n"
        return result
    return f"no contacts with such request: {args[0]}"
        
    
###########################################################################################    


def fun_name(fun):
    fun_dict = {
        "hello": hello,
        "good_bye": good_bye,
        "close": good_bye,
        "exit": good_bye,
        "add": add_func,
        "change": change_func,
        "dellete": dell_func,
        "dell": dell_func,
        "pagination": pagination,
        "phone": phone_func,
        "birthday": show_birthday,
        "show_all": show_all_func,
        "save": save_contacts,
        "load": load_contacts,
        "search": search_contacts
    }

    return fun_dict.get(fun)


def main():

    go_on = True
    
    address_book.load_contacts()
    
    while go_on:
        user_input = input("Listen You: ").lower()
        fun, args = parser(user_input)
        call_fun = fun_name(fun)

        if call_fun:

            text = call_fun(args)
            print(text)
            if text == "Good bye!":
                fun_name("save")()
                go_on = False

        else:
            print("No such command, try: add, change, show all")
            continue


main()
