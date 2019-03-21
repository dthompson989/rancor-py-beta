import os


def say_hello(name, comment):
    print("Hello, {}, {}".format(name, comment))


def calculate_interest():
    print("Now let's calculate some interest . . . ")
    amount = float(input("What is the principal amount?"))
    int_rate = float(input("What is the interest rate?"))
    no_years = int(input("How many years is the loan?"))

    total = (amount * (1 + ((int_rate/100) * no_years)) - amount)
    print("Interest: {:10.2f}".format(total))
    return


def display_types(name):
    new_list = list(name)
    new_set = set(name)
    new_tuple = tuple(name)

    print(type(new_list), new_list, 'Object Length:', len(new_list))
    print(type(new_set), new_set, 'Object Length:', len(new_set))
    print(type(new_tuple), new_tuple, 'Object Length:', len(new_tuple))
    return


def arithmetic():
    operand1 = int(input("Enter an operand: "))
    operand2 = int(input("Enter another operand: "))

    print("Addition:", operand1+operand2)
    print("Subtraction:", operand1-operand2)
    print("Multiplication:", operand1*operand2)
    print("Division (Float):", operand1/operand2)
    print("Division (Floor):", operand1//operand2)
    print("Modulus:", operand1 % operand2)
    print("Exponent:", operand1**operand2)
    return


def file_stuff():
    file_name = input("What is the file name?")
    file_action = input("Do you want to READ, WRITE, APPEND, or DELETE?")
    try:
        # READ will throw an error if the file doesn't exist
        if file_action.upper() == 'READ' or file_action.upper() == 'R':
            if os.path.exists(file_name):
                with open(file_name, "r") as file_object:
                    content = file_object.readlines()
                    print("File Content: \n", content)
            else:
                print("!!! That file does not exist !!!")
        # WRITE will create the file if it doesn't already exist
        elif file_action.upper() == 'WRITE' or file_action.upper() == 'W':
            with open(file_name, "w") as file_object:
                content = input("Enter your text \n")
                file_object.write(content)
        # APPEND will create the file if it doesn't already exist
        elif file_action.upper() == 'APPEND' or file_action.upper() == 'A':
            with open(file_name, "a") as file_object:
                content = input("Enter your text \n")
                file_object.write(content)
        # DELETE will throw an error if the file doesn't exist
        elif file_action.upper() == 'DELETE' or file_action.upper() == 'D':
            if os.path.exists(file_name):
                os.remove(file_name)
                print("File DELETED!")
            else:
                print("!!! That file does not exist !!!")
        else:
            print("You done messed up")
    except IOError:
        print("There was a problem with the file")
    return


if __name__ == '__main__':
    option = 0
    user_name = input("What is your name? ")
    say_hello(user_name, "you total goob")
    while option != 5:
        print("\nMain Menu:")
        print("1: Interest Calculator?")
        print("2: List, Set, Tuple?")
        print("3: Arithmetic?")
        print("4: File Operations?")
        print("5: EXIT")
        option = int(input("What would you like to do? "))
        if option == 1:
            calculate_interest()
        elif option == 2:
            display_types(user_name)
        elif option == 3:
            arithmetic()
        elif option == 4:
            file_stuff()
        else:
            print("Pick a number 1 through 5 idiot!")

# TODO finish this function
# the most recent variable is stored in '_' (the underscore)
# in python, a string is immutable, so dot notation works on a string object
# EXAMPLE: first_name = "David"
#          print(first_name.upper())
#          print(first_name.lower())
#          print(first_name)
# Lists are incredibly powerful and easy to use - http://www.techbeamers.com/python-list/
# EXAMPLE: listOfCountries = list(["India","United States","China","Germany"])
#          firstLetters = [ country[0] for country in listOfCountries ]
# The above example fills a list (array) without the need of a loop
# Object scope is local, unless initialized as a global object
# Importing Modules: from <module name> import *
#   OR from <module name> import <name1>, <name2>, etc
#   OR import <module name>

