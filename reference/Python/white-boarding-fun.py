#!usr/bin/python3.7
import sys
import ctypes
import gc
import pprint


if __name__ == '__main__':
    var1 = "some random string that is used to prove a point"
    var2 = var1

    # Output is getrefcount: 5 ctypes: 4
    print(f"var1 getrefcount: {sys.getrefcount(var1)}\nvar1 ctypes: {ctypes.c_long.from_address(id(var1)).value}")
    # Output is getrefcount: 5 ctypes: 4
    print(f"var2 getrefcount: {sys.getrefcount(var2)}\nvar2 ctypes: {ctypes.c_long.from_address(id(var2)).value}")

    # Lets see why these counts are so high
    pprint.pprint(gc.get_referrers(var1)[1])
    print("*************************************************\nGC!!!")
    print("*************************************************")
    gc.collect()
    pprint.pprint(gc.get_referrers(var1)[1])

""" Use this in Python Console . . .

import sys
import ctypes
import gc
import pprint

var1 = "some random string that is used to prove a point"
var2 = var1

print(f"var1 getrefcount: {sys.getrefcount(var1)}\nvar1 ctypes: {ctypes.c_long.from_address(id(var1)).value}")
print(f"var2 getrefcount: {sys.getrefcount(var2)}\nvar2 ctypes: {ctypes.c_long.from_address(id(var2)).value}")

pprint.pprint(gc.get_referents(var1)) 
"""
