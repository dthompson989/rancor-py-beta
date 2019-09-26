#!usr/bin/python
"""This is basically a test script for radon complexity analysis"""


def a_little_complex():
    """O(n) Complexity"""
    print("O(n) Complexity")
    little_list = ["Just ", "A ", "Little ", "List"]
    for word in little_list:
        print(word)


def more_complex():
    """O(n^2) Complexity"""
    print("O(n^2) Complexity")
    multi_list = [["This ", "is ", "a "],
                  ["multi", "-", "dimensional"],
                  ["list ", "with ", "gusto"]]
    for sentence in multi_list:
        for word in sentence:
            print(word)


def stupid_complex():
    """O(n!) Complexity . . . need to think about a sensible way to do this"""
    print("O(n!) Complexity . . .")
    print("Sorry . . . nothing yet!")


if __name__ == '__main__':
    a_little_complex()
    more_complex()
    stupid_complex()
