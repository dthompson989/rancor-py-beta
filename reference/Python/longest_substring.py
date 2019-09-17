#!usr/bin/python3
"""This will find the length of the longest substring without repeating for any given string"""


def str_length(string):
    count = 0
    if string:
        temp_list = list()
        for char in string.lower():
            if char in temp_list:
                temp_list = temp_list[temp_list.index(char)+1:]
                temp_list.append(char)
            else:
                temp_list.append(char)
                if count < len(temp_list):
                    count = len(temp_list)

    return count


if __name__ == '__main__':
    print("Hey Turd . . . ")
    input_str = str(input("Enter a string: "))
    print(str_length(input_str))
