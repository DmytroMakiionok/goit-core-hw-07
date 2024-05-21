from datetime import datetime, timedelta
from collections import UserDict

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    def __init__(self, value):
        super().__init__(value)
        if not value:
            raise ValueError("Name cannot be empty")

class Phone(Field):
    def __init__(self, value):
        super().__init__(value)
        if not self.validate_phone(value):
            raise ValueError("Invalid phone number format")

    def validate_phone(self, phone):
        return len(phone) == 10 and phone.isdigit()

class Birthday(Field):
    def __init__(self, value):
        try:
            self.value = datetime.strptime(value, "%d.%m.%Y")
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        new_phone = Phone(phone)
        self.phones.append(new_phone)
        return new_phone

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(str(i) for i in self.phones)}, birthday: {self.birthday}"

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)     
        except KeyError:
            return "Enter the argument for the command"
        except IndexError:
            return "Invalid index in sequence"
        except ValueError:
            return "ValueError"

    return inner

@input_error
def parse_input(user_input):
    cmd, *args = user_input.split()
    return cmd, args
@input_error
def add_contact(args, book: AddressBook): 
    name = args[0]
    phone = args[1]
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    if phone:
        record.add_phone(phone)
    return message
@input_error
def change_contact(args, book: AddressBook):
    name = args[0]
    phone = args[1]
    if name in book.data:
        book.data[name].phones = [Phone(phone)]
        return "Contact updated."
    else:
        return "Contact not found."
@input_error
def get_phone(args, book: AddressBook):
    name = args[0]
    if name in book.data:
        return f"The phone number for {name} is {book.data[name].phones[0]}."
    else:
        return "Contact not found."
@input_error
def list_all_contacts(book: AddressBook):
    if not book:
        return "No contacts found."
    else:
        return "\n".join([str(record) for record in book.values()])
@input_error
def add_birthday(args, book: AddressBook):
    name = args[0]
    birthday = args[1]
    record = book.find(name)
    message = "Birthday updated."
    if record is None:
        return "Contact not found."
    record.add_birthday(birthday)
    return message

@input_error
def show_birthday(args, book: AddressBook):
    name = args[0]
    record = book.find(name)
    if record and record.birthday:
        return f"The birthday of {name} is {record.birthday}."
    elif record and not record.birthday:
        return f"No birthday set for {name}."
    else:
        return f"Contact {name} not found."

@input_error    
def date_to_string(date):
    return date.strftime("%d.%m.%Y")
    
@input_error
def get_upcoming_birthdays(book: AddressBook, days=7):
    upcoming_birthdays = []
    today = date.today()
    for record in book.values():
        if record.birthday:
            conf_date = record.birthday.value.replace(year=today.year).date()
            difference = (conf_date - today).days
            if 0 <= difference <= days: 
                upcoming_birthdays.append({"name": record.name.value, "congratulation_date": date_to_string(conf_date)})
    return upcoming_birthdays
    
def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break

        elif command == "hello":
            print("How can I help you?")

        elif command == "add":
            print(add_contact(args, book))

        elif command == "change":
            print(change_contact(args, book))

        elif command == "phone":
            print(get_phone(args, book))

        elif command == "all":
            print(list_all_contacts(book))

        elif command == "add-birthday":
            print(add_birthday(args, book))

        elif command == "show-birthday":
            print(show_birthday(args, book))

        elif command == "birthdays":
            print(get_upcoming_birthdays(book))

        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()
