# Author: Madan Y N
# Undergraduate EE IITB (2024)

"""This file contains configuration of P-core of Intel Alder Lake 
processor based on Golden Cove microarchictecure. SimpleOpts 
wrapper is used to set up command line options from each individual 
class. """

import m5
from m5.objects import *
from core import *
from caches import *

class MySystem(System):
    # Choose the cpu model from core
    _CPUModel = VerbatimCPU

    def __init__(self):
        super(MySystem, self).__init__()

        self.clk_domain = SrcClockDomain()
        self.clk_domain.clock = '5.2GHz'
        self.clk_domain.voltage_domain = VoltageDomain()

        self.mem_mode = 'timing'
        mem_size = '32GB'
        self.mem_ranges = [AddrRange('100MB'), #kernel
                           AddrRange(0xC0000000, size=0x100000), #IO
                           AddrRange(Addr('4GB'), size = mem_size) #processes
                           ]
        
        self.cpu = self._CPUModel()

        """ Memory bus
        bus width set double as that of skylake-config """
        self.membus = SystemXBar(width = 384)
        self.membus.badaddr_responder = BadAddr()
        self.membus.default = Self.badaddr_responder.pio

        self.system_port = self.membus.cpu_side_ports

        """L1 instruction and data cache"""
        self.cpu.icache = L1ICache()
        self.cpu.dcache = L1DCache()

        self.cpu.icache.connectCPU(self.cpu)
        self.cpu.dcache.connectCPU(self.cpu)

        """memory bus width double as that in skylake-config"""
        self.l2bus = L2XBar(width = 384)

        self.cpu.icache.connectBus(self.l2bus)
        self.cpu.dcache.connectBus(self.l2bus)

        self.cpu.l2cache = L2Cache()
        # self.cpu.mmucache = MMUCache()
        # self.cpu.mmucache.connectCPU(self.cpu)
        self.cpu.l2cache.connectCPUSideBus(self.l2bus)

        self.l3bus = L2XBar(width = 384,
                            snoop_filter = SnoopFilter(max_capacity='32MB'))
        
        self.cpu.l2cache.connectMemSideBus(self.l3bus)
        # self.cpu.mmucache.connectMem(self.l3bus)

        self.l3cache = L3Cache()
        self.l3cache.connectCPUSideBus(self.l3bus)
        self.l3cache.connectMemSideBus(self.membus)

        self.cpu.createInterruptController()

        # self.cpu.interrupts[0].pio = self.membus.mem_side_ports
        # self.cpu.interrupts[0].int_requestor = self.membus.cpu_side_ports
        # self.cpu.interrupts[0].int_responder = self.membus.mem_side_ports

        self.createMemoryControllersDDR4()

    def createMemoryControllersDDR4(self):
        self._createMemoryControllers(1, DDR4_2400_16x4)

    def _createMemoryControllers(self, num, cls):
        kernel_controller = self._createKernelMemoryController(cls)

        ranges = self._getInterleaveRanges(self.mem_ranges[-1], num, 6, 20)
        self.mem_cntrls = [
            MemCtrl(dram = cls(range = ranges[i]), port = self.membus.mem_side_ports)
            for i in range(num)
        ] + [kernel_controller]

    def _createKernelMemoryController(self, cls):
        return MemCtrl(dram = cls(range = self.mem_ranges[0]), port = self.membus.mem_side_ports)

    def _getInterleaveRanges(self, rng, num, intlv_low_bit, xor_low_bit):
        from math import log
        bits = int(log(num, 2))
        if 2**bits != num:
            m5.fatal("Non-power of two number of memory controllers")

        intlv_bits = bits
        ranges = [
            AddrRange(start=rng.start,
                    end=rng.end,
                    intlvHighBit = intlv_low_bit + intlv_bits - 1,
                    xorHighBit = xor_low_bit + intlv_bits - 1,
                    intlvBits = intlv_bits,
                    intlvMatch = i)
                for i in range(num)
            ]

        return ranges

    def setTestBinary(self, binary_path):
        """Set up the SE process to execute the binary at binary_path"""
        from m5 import options
        self.cpu.workload = Process(
                        cmd = [binary_path])
        self.cpu.createThreads()
