# Author: Madan Y N
# Undergraduate EE IITB (2024)

"""
Top-level file to run simulations on GLC
Path to the binary is given here - Change binary to run appropriate benchmark
"""

import m5
from m5.objects import *
import argparse
from se  import MySystem
from core import *

#valid_configs = [VerbatimCPU, TunedCPU, UnConstrainedCPU]
#valid_configs = {cls.__name__[:-3]:cls for cls in valid_configs}

#parser = argparse.ArgumentParser()
#parser.add_argument('config', choices = valid_configs.keys())
#parser.add_argument('binary', type = str, help = "Path to binary to run")
#args = parser.parse_args()

class TestSystem(MySystem):
    _CPUModel = VerbatimCPU

binary = 'tests/my_tests/primes_arm'
system = TestSystem()
system.workload = SEWorkload.init_compatible(binary)

process = Process()
process.cmd = [binary]
system.cpu.workload = process
system.cpu.createThreads()

root = Root(full_system = False, system = system)
m5.instantiate()
exit_event = m5.simulate()

print('Exiting @ tick {} because {}'
      .format(m5.curTick(), exit_event.getCause()))
