# Author: Madan Y N
# Undergraduate EE IITB (2024)

"""
The file contains decription of a single threaded(No HyperThreading) 
Golden Cove core to be used in Gem5 configuration script. SimpleOpts 
wrapper is used to set up command line options from each individual 
class.
"""

import m5
from m5.objects import *
from m5.objects import FUDesc
import math

class port0(FUDesc):
    pass

class port1(FUDesc):
    pass

class port2(FUDesc):
    pass

class port3(FUDesc):
    pass

class port4(FUDesc):
    pass

class port5(FUDesc):
    pass

class port6(FUDesc):
    pass

class port7(FUDesc):
    pass

class port8(FUDesc):
    pass

class port9(FUDesc):
    pass

class port10(FUDesc):
    pass

class port11(FUDesc):
    pass

class ExecUnits(FUPool):
    FUList = [port0(), port1(), port2(), port3(), port4(), port5(), port6(), port7(), port8(), port9(), port10(), port11()]

