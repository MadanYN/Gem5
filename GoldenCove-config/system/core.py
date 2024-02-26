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

""" The classes port0 through port11 are the execution units of Golden Cove. The functional units are described in Intel's
official document and also in https://chipsandcheese.com/2021/12/02/popping-the-hood-on-golden-cove/ blogpost. Latency of
the functional units are mostly taken from Agner Fog's microarchitecture blog """


""" LEA(Load Effective Address) unit is not available in gem5. There are no functional units describing 'Integer Shift' and 
'JMP' as well. My guess is that this instruction is handled by IntAlu itself. So I have added another IntAlu into port0 """
class port0(FUDesc):
    opList = [opDesc(opClass = 'IntAlu', opLat = 1, pipelined = True),
              opDesc(opClass = 'IntAlu', opLat = 1, pipelined = True),
              opDesc(opClass = 'SimdMultAcc', opLat = 10, pipelined = True),
              opDesc(opClass = 'SimdFloatMultAcc', opLat = ,pipelined = True),
              opDesc(opClass = 'SimdShift', opLat = , pipelined = True),
              opDesc(opClass = 'SimdFloatDiv', opLat = , pipelined = True),
              opDesc(opClass = 'SimdDiv', opLat = , pipelined = True),
              opDesc(opclass = 'SimdAlu', opLat = , pipelined = True),
              opDesc(opclass = 'SimdFloatAlu', opLat = , pipelined = True)
              ]

""" Shuffle functional unit is not described in gem5 """
class port1(FUDesc):
    opList = [opDesc(opClass = 'IntAlu', opLat = 1, pipelined = True),
              opDesc(opClass = 'IntMul', opLat = 3, pileined = True),
              opDesc(opClass = 'IntDiv', opLat = 15, pipelined = True),
              opDesc(opClass = 'FloatMult', opLat = 4, pipelined = True),
              opDesc(opClass = 'SimdMultAcc', opLat = 10, pipelined = True),
              opDesc(opClass = 'SimdFloatMultAcc', opLat = ,pipelined = True),
              opDesc(opClass = 'SimdShift', opLat = , pipelined = True),
              opDesc(opClass = 'SimdFloatDiv', opLat = , pipelined = True),
              opDesc(opClass = 'SimdDiv', opLat = , pipelined = True),
              opDesc(opclass = 'SimdAlu', opLat = , pipelined = True),
              opDesc(opclass = 'SimdFloatAlu', opLat = , pipelined = True),
              opDesc(opClass = 'FloatAdd', opLat = 2, pipelined = True),
              opDesc(opClass = 'SimdFloatAdd', opLat = , pipelined = True)
              ]

class port2(FUDesc):
    opList = [opDesc(opClass = 'memRead', opLat = , pipelined = True),
              opDesc(opClass = 'FloatMemRead', opLat = , pipelined = True)
              ]

class port3(FUDesc):
    opList = [opDesc(opClass = 'memRead', opLat = , pipelined = True),
              opDesc(opClass = 'FloatMemRead', opLat = , pipelined = True)
              ]

class port4(FUDesc):
    opList = [opDesc(opClass = 'memWrite', opLat = , pipelined = True),
              opDesc(opClass = 'FloatMemWrite', opLat = , pipelined = True)
              ]

""" FMA512 functional units which are part of AVX-512 Extensions are not described in gem5. 
I have added FMA(FMA256) instead of that 
Shuffle functional unit is not described in gem5 """
class port5(FUDesc):
    opList = [opDesc(opClass = 'IntAlu', opLat = 1, pipelined = True),
              opDesc(opClass = 'IntMul', opLat = 1, pipelined = True),
              opDesc(opClass = 'SimdMultAcc', opLat = 10, pipelined = True),
              opDesc(opClass = 'SimdFloatMultAcc', opLat = ,pipelined = True),
              opDesc(opclass = 'SimdAlu', opLat = , pipelined = True),
              opDesc(opclass = 'SimdFloatAlu', opLat = , pipelined = True),
              opDesc(opclass = 'Matrix', opLat = , pipelined = True),
              """ The below functional units are part of AMX (Advanced Matrix Extensions) """
              opDesc(opClass = 'MatrixMov', opLat = , pipelind = True),
              opDesc(opClass = 'MatrixOp', opLat = , pipelined = True),
              opDesc(opClass = 'SimdMatMultAcc', opLat = , pipelined = True),
              opDesc(opClass = 'SimdFloatMatMultAcc', opLat = , pipeined = True)
              ]

""" Two IntAlu units to account for LEA, Shift and JMP """
class port6(FUDesc):
    opList = [opDesc(opClass = 'IntAlu', opLat = 1, pipelined = True),
              opDesc(opClass = 'IntAlu', opLat = 1, pipelined = True)
              ]

class port7(FUDesc):
    opList = [opDesc(opClass = 'memWrite', opLat = , pipelined = True),
              opDesc(opClass = 'FloatMemWrite', opLat = , pipelined = True)
              ]

class port8(FUDesc):
    opList = [opDesc(opClass = 'memWrite', opLat = , pipelined = True),
              opDesc(opClass = 'FloatMemWrite', opLat = , pipelined = True)
              ]

class port9(FUDesc):
    opList = [opDesc(opClass = 'memWrite', opLat = , pipelined = True),
              opDesc(opClass = 'FloatMemWrite', opLat = , pipelined = True)
              ]

class port10(FUDesc):
    opList = [opDesc(opClass = 'IntAlu', opLat = 1, pipelined = True)]

class port11(FUDesc):
    opList = [opDesc(opClass = 'memRead', opLat = , pipelined = True),
              opDesc(opClass = 'FloatMemRead', opLat = , pipelined = True)
              ]    

class ExecUnits(FUPool):
    FUList = [port0(), port1(), port2(), port3(), port4(), port5(), port6(), port7(), port8(), port9(), port10(), port11()]

""" The params in IndirectPred classe are taken directly from branch predictor classes of skylake-config """
class IndirectPred(SimpleIndirectPredictor):
    indirectSets = 128 # Cache sets for indirect predictor
    indirectWays = 4 # Ways for indirect predictor
    indirectTagSize = 16 # Indirect target cache tag bits
    indirectPathLength = 7 # Previous indirect targets to use for path history
    indirectGHRBits = 16 # Indirect GHR number of bits

""" The MultiperspectivePerceptronTAGE64KB branch predictor is the most powerful(in terms of hardware resources used) 
perceptron based branch predictor. Intel has only disclosed that a varient of hashed perceptron branch predictor has 
been used in Golden Cove. """
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

    """ Intel Core2 and Intel Atom architectures both have 16 pipeline stages and Agner Fog's blog claims that it was
    followed till skylake icelake. AnandTech's blog mentions that P core of Alder Lake has increased number of pipeline 
    stages, so I have taken the number of pipeline stages to be 20 """

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