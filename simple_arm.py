#simple in-order x86 single-core cpu architecture with two-level cache architecture in sys emulation mode

import m5
from m5.objects import *
from caches import *
#m5.util.addToPath("../../../")
m5.util.addToPath("")

from common import SimpleOpts

import argparse

#parser = argparse.ArgumentParser(description='A simple system with 2-level cache.')
# parser.add_argument("binary", default="", nargs="?", type=str,
#                     help="Path to the binary to execute.")
#parser.add_argument("--l1i_size",
#                    help=f"L1 instruction cache size. Default: 16kB.")
#parser.add_argument("--l1d_size",
#                    help="L1 data cache size. Default: Default: 64kB.")
#parser.add_argument("--l2_size",
#                    help="L2 cache size. Default: 256kB.")

#options = parser.parse_args()
args = SimpleOpts.parse_args()

system = System() #System() class contains all info about the system being simuated
system.clk_domain = SrcClockDomain()
system.clk_domain.clock = '1GHz'
system.clk_domain.voltage_domain = VoltageDomain()

system.mem_mode = 'timing'
system.mem_ranges = [AddrRange('1024MB')]
system.cpu = ArmTimingSimpleCPU() #All instructions except memory requests executed in single cycle

#creating caches
system.cpu.icache = L1ICache(args)
system.cpu.dcache = L1DCache(args)

#connecting caches to cpu ports
system.cpu.icache.connectCPU(system.cpu)
system.cpu.dcache.connectCPU(system.cpu)

system.membus = SystemXBar() #Bus interconnecting cpu and memory

#------------------ this part is for system with no cache architecture----#
# system.cpu.icache_port = system.membus.cpu_side_ports
# system.cpu.dcache_port = system.membus.cpu_side_ports
#-------------------------------------------------------------------------#

#connecting L1 caches to L2 bus
system.l2bus = L2XBar()
system.cpu.icache.connectBus(system.l2bus)
system.cpu.dcache.connectBus(system.l2bus)

#L2 cache
system.l2cache = L2Cache(args)
system.l2cache.connectCPUSideBus(system.l2bus)
system.l2cache.connectMemSideBus(system.membus)

system.cpu.createInterruptController()
system.system_port = system.membus.cpu_side_ports

#memory controller
system.mem_ctrl = MemCtrl()
system.mem_ctrl.dram = DDR3_1600_8x8()    
system.mem_ctrl.dram.range = system.mem_ranges[0]
system.mem_ctrl.port = system.membus.mem_side_ports

#binary = 'tests/test-progs/hello/bin/arm/linux/hello'
binary = 'tests/my_tests/primes_arm'
system.workload = SEWorkload.init_compatible(binary)

# system.workload = SEWorkload.init_compatible(options.binary)
process = Process()
process.cmd = [binary]
system.cpu.workload = process
system.cpu.createThreads()

root = Root(full_system = False, system = system)
m5.instantiate()
print("Beginning simulation!")
exit_event = m5.simulate()

print('Exiting @ tick {} because {}'
      .format(m5.curTick(), exit_event.getCause()))
