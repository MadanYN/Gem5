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

""" The params in IndirectPred classe are taken directly from branch predictor classes of skylake-config """
class IndirectPred(SimpleIndirectPredictor):
    indirectSets = 128 # Cache sets for indirect predictor
    indirectWays = 4 # Ways for indirect predictor
    indirectTagSize = 16 # Indirect target cache tag bits
    indirectPathLength = 7 # Previous indirect targets to use for path history
    indirectGHRBits = 16 # Indirect GHR number of bits

""" The MultiperspectivePerceptronTAGE64KB branch predictor is the most powerful(in terms of hardware resources used) perceptron based branch
predictor. Intel has only disclosed that a varient of hashed perceptron branch predictor has been used in Golden Cove. """
class BranchPred(MultiperspectivePerceptronTAGE64KB):
    """number of entries in the BTB
    Haswell had a BTB of size 4096, accurate size of BTB is not available for modern architectures """
    numEntries = 8192
    """The number of tag bits used is same as that in Haswell architecture"""
    tagBits = 21
    indirectBranchPred = IndirectPred()


depth = 4

class VerbatimCPU(DerivO3CPU):
    """ Uncalibrated: Configured based on micro-architecture documentation """

    branchPred = BranchPred()

    """ Intel Core2 and Intel Atom architectures both have 16 pipeline stages and Agner Fog's blog claims that it was followed till skylake
    icelake. AnandTech's blog mentions that P core of Alder Lake has increased number of pipeline stages, so I have taken the number of 
    pipeline stages to be 20 """

    # Pipeline delays
    # https://gem5-users.gem5.narkive.com/LNMJQ1M5/model-deeper-pipeline-in-x86#post2
    # to model 20 stage pipeline choose depth parameter as 4
    fetchToDecodeDelay = depth
    decodeToRenameDelay = 1
    renameToIEWDelay = 3*depth
    iewToCommitDelay = 2* depth

    forwardComSize = 20
    backComSize = 20

    fuPool = ExecUnits()

    # Pipeline widths
    fetchWidth = 8
    decodeWidth = 6
    renameWidth = 6
    dispatchWidth = 6
    issueWidth = 12
    wbWidth = 8
    commitWidth = 8
    squashWidth = 8

    fetchWidth = 24
    """Fetch Queue size same as that in skylake-config"""
    fetchQueueSize = 50
    numRobs = 1
    numPhysIntRegs = 280
    numPhysFloatregs = 332
    """Golden Cove has three different instruction queues
        1. Unified Math Inst Queue - 97 entries
        2. Load Inst Queue - 70
        3. Store Inst Queue - 38 
    Which totals to 205 entries """
    numIQEntries = 205
    numROBEntries = 512
    LQEntries = 192
    SQEntries = 118




