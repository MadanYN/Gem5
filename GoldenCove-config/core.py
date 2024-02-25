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

"""The params in IndirectPred classe are taken directly from branch predictor classes of skylake-config"""
class IndirectPred(SimpleIndirectPredictor):
    indirectSets = 128 # Cache sets for indirect predictor
    indirectWays = 4 # Ways for indirect predictor
    indirectTagSize = 16 # Indirect target cache tag bits
    indirectPathLength = 7 # Previous indirect targets to use for path history
    indirectGHRBits = 16 # Indirect GHR number of bits

"""The MultiperspectivePerceptronTAGE64KB branch predictor is the most powerful(in terms of hardware resources used) perceptron based branch
predictor. Intel has only disclosed that a varient of hashed branch predictor has been used in Golden Cove.
"""
class BranchPred(MultiperspectivePerceptronTAGE64KB):
    """number of entries in the BTB
    Haswell had a BTB of size 4096, accurate size of BTB is not available for modern architectures
    """
    numEntries = 8192
    """The number of tag bits used is same as that in Haswell architecture"""
    tagBits = 21
    indirectBranchPred = IndirectPred()

class VerbatimCPU(DerivO3CPU):
    """ Uncalibrated: Configured based on micro-architecture documentation """

    branchPred = BranchPred()

    