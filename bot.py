from telegram.ext import Updater, CommandHandler

"""
Defining some key names here ..
"""
file = 'Books.csv'
commands_file = "commands.txt"
updater = Updater('630548015:AAGLsP7J1CLW7d36xOfC_zhvwXcgZp1Ptlg')
creds = 'credits.txt'


def team(bot, update):
    """
    Reads credits from a .txt file and shows them to the user.
    """
    with open(creds, "r") as team:
        update.message.reply_text(team.read())


def hello(bot, update):
    """
    Greets user with his telegram name.
    """
    update.message.reply_text(
        'Hello, {}'.format(update.message.from_user.first_name))


def commands(bot, update):
    """
    Reads a .txt file with description of all commands and
    gives it to the user.
    """
    with open(commands_file, "r") as all_commands:
        update.message.reply_text(all_commands.read())


def give(bot, update, args):
    """
    Adds a book to general list.
    """
    if len(args) == 2:
        write_csv(fetch_bookdata(update.message.text,
                                 update.message.from_user.username))
        update.message.reply_text('Your book was added to list!')
    else:  # exception
        update.message.reply_text('Check the correction of your input!')


def fetch_bookdata(user_string, user_name):
    """
    Collects data from user input and adds some corrections to it.
    """
    user_string = user_string.split()[1:]  # fetches necessary data from input
    user_name = "@" + user_name  # adds '@' symbol to identify user
    user_string.append(user_name)
    user_string.append('Free')  # states that a book has a status "Free"
    return user_string


def write_csv(new_string):
    """
    Writes data into .csv file.
    """
    with open('Books.csv', 'a') as books:
        books.write(','.join(new_string) + '\n')


def read_csv(file_name):
    """
    Reads data from .csv file.
    """
    with open(file_name, 'r') as file:
        file = file.readlines()
    for i in range(len(file)):
        file[i] = file[i].replace(',', ' | ')
    file = sorted(file, key=lambda x: x[0].capitalize())  # alphabetic sort
    return file


def list_all(bot, update):
    """
    Gives a database of all books to the user.
    """
    result = ''.join(read_csv(file))
    if len(result) != 0:
        update.message.reply_text('All books are:\n' + result)
    else:  # exception
        update.message.reply_text('There are no books now :(')


def generate(truth=',Borrowed'):
    """
    Helping function to change key arguments when needed.
    """
    def borrowed(bot, update, args):
        """
        Changes last value in database of books depending on 'truth' argument.

        1984 | J.Orwell | @pazyniuk | Free --->
        ---> 1984 | J.Orwell | @pazyniuk | Borrowed

        1984 | J.Orwell | @pazyniuk | Borrowed --->
        ---> 1984 | J.Orwell | @pazyniuk | Free
        """
        csv_file = read_csv(file)
        user_string = update.message.text.split()[1:]
        if len(user_string) == 2:
            user_string.append('@' + update.message.from_user.username)
            for i in range(len(csv_file)):
                if user_string[0] in csv_file[i] and\
                   user_string[1] in csv_file[i] and\
                   user_string[2] in csv_file[i]:
                    csv_file[i] = ','.join(user_string) + truth + '\n'
                    update.message.reply_text('Status changed successfully!')
                else:
                    csv_file[i] = csv_file[i].replace(' | ', ',')
            update_csv(csv_file)
        else:  # exception
            update.message.reply_text('Check the correction of your input!')
    return borrowed


def update_csv(lst):
    """
    Updates .csv file with new data by rewriting its whole structure.
    """
    with open(file, 'w') as csv_file:
        for string in lst:
            csv_file.write(string)
        csv_file.close()


def search(bot, update, args):
    """
    Searches for keyword inputed by user in database of books.
    """
    csv_file = read_csv(file)
    user_string = update.message.text.split()
    result = str()
    if len(user_string) == 2:
        for i in range(len(csv_file)):
            csv_file[i] = csv_file[i].replace(' | ', ',')
            old_string = csv_file[i]
            csv_file[i] = csv_file[i].split(',')[:2]
            elem = ','.join(csv_file[i])
            if user_string[1] in elem:
                result += old_string.replace(',', ' | ')
            else:
                continue
        if result != str():
            update.message.reply_text(
                'The book(-s) you searched for are: \n' + result)
        else:
            update.message.reply_text('No books found on this result')
    else:  # exception
        update.message.reply_text('Check the correction of your input!')


def main():
    updater.dispatcher.add_handler(
        CommandHandler(
            'hello',
            hello))
    updater.dispatcher.add_handler(
        CommandHandler(
            'credits',
            team))
    updater.dispatcher.add_handler(
        CommandHandler(
            'start',
            commands))
    updater.dispatcher.add_handler(
        CommandHandler(
            'give',
            give,
            pass_args=True))
    updater.dispatcher.add_handler(
        CommandHandler(
            'borrowed',
            generate(),
            pass_args=True))
    updater.dispatcher.add_handler(
        CommandHandler(
            'returned',
            generate(',Free'),
            pass_args=True))
    updater.dispatcher.add_handler(
        CommandHandler(
            'list_all',
            list_all))
    updater.dispatcher.add_handler(
        CommandHandler(
            'search',
            search,
            pass_args=True))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()  # launch
