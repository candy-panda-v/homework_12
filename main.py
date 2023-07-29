import classes


address_book = classes.AddressBook()
bot_working = True
save_path = 'address_book.bin'


def input_error(func):
    def inner(*args, **kwargs):
        consecutive_errors = 0
        while bot_working:
            try:
                return func(*args, **kwargs)
            except UnboundLocalError:
                print('Enter command')
            except TypeError:
                print('Enter name and phone separated by a space!')
            except KeyError:
                print('This name was not found!')
            except IndexError:
                print('This name was found! Enter another name.')
            except Exception as e:
                print('Error:', e)
            consecutive_errors += 1
            if consecutive_errors >= 5:
                print("Exiting due to consecutive wrong commands.")
                close()
                break
    return inner


def start():
    address_book.load_from_file(save_path)
    print("How may I help you?")

def helper():
    res = ''
    for key in COMMANDS.keys():
        res += f"{key}\n"
    return "Available bot function:\n" + res


def close():
    global bot_working
    bot_working = False
    address_book.save_to_file(save_path)
    return ("Good bye! Bot stopped.")


def hello():
    return ('How can I help you?')


@input_error
def add_record(name, phone='', birthday=''):
    rec_name = classes.Name()
    rec_name.value = name

    rec_phone = classes.Phone()
    rec_phone.value = phone

    rec_bd = classes.Birthday()
    rec_bd.value = birthday

    rec = classes.Record(rec_name, rec_phone, rec_bd)

    address_book.addRecord(rec)
    return str(rec)


def change_phone(name, old_phone, new_phone):
    rec = address_book[name]
    o_ph = classes.Phone()
    o_ph.value = old_phone
    n_ph = classes.Phone()
    n_ph.value = new_phone
    if o_ph.value not in [phone.value for phone in rec.phones]:
        print("This phone was not found!")
    else:
        rec.change_phone(o_ph, n_ph)
        return rec.print_record()


def add_phone(name, phone):
    rec = address_book[name]
    ph = classes.Phone()
    ph.value = phone
    rec.add_phone(ph)
    return str(rec)


def add_birthday(name, birthday):
    rec = address_book[name]
    bd = classes.Birthday()
    bd.value = birthday
    rec.add_birthday(bd)
    return str(rec)


def delete_phone(name, phone):
    rec = address_book[name]
    ph = classes.Phone()
    ph.value = phone
    rec.del_phone(ph)
    return str(rec)


def days_to_birthday(name):
    rec = address_book[name]
    return rec.days_to_birthday()


def showall():
    return address_book


def find(string: str):
    return address_book.find(string)


def command_parse(user_input):
    words = user_input.lower().split()
    for i in range(len(words)):
        for key, cmd in COMMANDS.items():
            if key in " ".join(words[i:]):
                return cmd, words[i + 1:]
    return "Unknown command, try again", []


COMMANDS = {'hello': hello,
            'days to bd': days_to_birthday,
            'add phone': add_phone,
            'add birthday': add_birthday,
            'change phone': change_phone,
            'delete phone': delete_phone,
            'find ': find,
            'show all': showall,
            'good bye': close,
            'exit': close,
            'close': close,
            'add': add_record,
            'help': helper,
            }


@input_error
def main():
    start()
    while bot_working:
        s = input()
        command, arguments = command_parse(s)
        print(command(*arguments))


if __name__ == '__main__':
    main()
