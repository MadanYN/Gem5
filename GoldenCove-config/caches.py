# Author: Madan Y N
# Undergraduate EE IITB (2024)

"""
This file contains L1I, L1D, L2 and L3 caches to be used in the gem5
configuration script. SimpleOpts wrapper is used to set up command line
options from each individual class.
"""

import m5
from m5.objects import Cache, PIFPrefetcher, L2XBar


"""All options can be found at src/mem/cache/BaseCache.py in the offical gem5 repo"""

class PrefetchCache(Cache):

    def __init__(self):
        super(PrefetchCache, self).__init__()
        self.prefetcher = PIFPrefetcher()
        self.replacement_policy = TreePLRURP()
        self.prefetch_on_access = True
        """Tag and data are accessed parallely"""
        self.sequential_access = False 

class L1Cache(PrefetchCache):
    """Base L1 cache with default params"""

    assoc = 12

    tag_latency = 5
    data_latency = 5
    response_latency = 1

    """The MSHR values are taken from chips and cheese blogpost"""
    mshr = 16
    # tgts_per_mshr = 16
    # write_buffers = 56
    # demand_mshr_reserve = 8

    def __init__(self):
        super(L1Cache, self).__init__()
    
    def connectBus(self, bus):
        """Connect cache to memory-side bus"""
        self.mem_side = bus.cpu_side_ports
    
    def connectCPU(self, cpu):
        """This has to be implemented in the L1I and L1D subclasses"""
        raise NotImplementedError

class L1ICache(L1Cache):
    """L1 instruction cache with default values"""

    size = '48KB'
    """icache memory is read-only from cpu point of view"""
    is_read_only = True

    def __init__(self):
        super(L1ICache, self).__init__()

    def connectCPU(self, cpu):
        self.cpu_side = cpu.icache_port

class L1DCache(L1Cache):
    """L1 data cache with default values"""

    size = '48KB'

    """The write buffer and write allocator params are taken as it is from gem5-skylake-config"""
    write_buffers = 128

    write_allocator = WriteAllocator()
    write_allocator.coalesce_limit = 2
    write_allocator.no_allocate_limit = 8
    write_allocator.delay_threshold = 8

    def __init__(self):
        super(L1DCache, self).__init__()

        def connectCPU(self, cpu):
            self.cpu_side = cpu.dcache_port

class MMUCache(PrefetchCache):
    """These parameters are same as those in gem5-skylake-config"""
    size = '8KB'
    assoc = 8
    tag_latency = 1
    data_latency = 1
    response_latency = 1
    mshrs = 32
    tgts_per_mshr = 8

    def __init__(self):
        super(MMUCache, self).__init__()

    def connectCPU(self, cpu):
        self.mmubus = L2XBar()
        self.cpu_side = self.mmubus.mem_side_ports
        for tlb in [cpu.itb, cpu.dtb]:
            self.mmubus.cpu_side_ports = tlb.walker.port
        
    def connectBus(self, bus):
        self.mem_side = bus.cpu_side_ports

class L1iTLB(PrefetchCache):
    """L1 instruction TLB with defaut values"""

    size = '2KB'
    assoc = 8
    """Latency numbers are not available yet. The chosen tag and data latencies are lesser 
    than those of L1I and L1D caches because of the smaller size of TLB
    """
    tag_latency = 2
    data_latency = 2
    response_latency = 1
    mshrs = 8
    tgts_per_mshr = 8

    def __init__(self):
        super(L1iTLB, self).__init__()
    
    def connectMem(self, bus):
        self.mem_side = bus.cpu_side_ports

    def connectCPU(self, cpu):
        """Connect cpu side port to the instruction table walker port of cpu"""
        self.cpu_side = cpu.itb.walker.port


class L1dTLB(PrefetchCache):
    """L1 data TLB with default values"""

    size = '768B'
    assoc = 6
    """Latency numbers are not available yet. The chosen tag and data latencies are lesser 
    than those of L1I and L1D caches because of the smaller size of TLB
    """
    tag_latency = 2
    data_latency = 2
    response_latency = 1
    mshrs = 8
    tgts_per_mshr = 8

    def __init__(self):
        super(L1iTLB, self).__init__()

    def connectMem(self, bus):
        self.mem_side = bus.cpu_side_ports

    def connectCPU(self, cpu):
        """Connect cpu side port to the data table walker port of cpu"""
        self.cpu_side = cpu.dtb.walker.port

class L2TLB(PrefetchCache):
    """L2 TLB with default values"""

    size = '16KB'
    assoc = 16
    tag_latency = 7
    data_latency = 7
    response_latency = 1
    mshrs = 16
    tgts_per_mshr = 8

    def connectCPUSideBus(self, bus):
        self.cpu_side = bus.mem_side_ports

    def connectMemSideBus(self, bus):
        self.mem_side = bus.cpu_side_ports



class L2Cache(PrefetchCache):
    """L2 Cache with default values"""

    size = '1280KB'
    assoc = 10
    tag_latency = 15
    data_latency = 15
    response_latency = 1
    mshrs = 48
    # tgts_per_mshr = 16
    # write_buffers = 256

    def __init__(self):
        super(L2Cache, self).__init__()
    
    def connectCPUSideBus(self, bus):
        self.cpu_side = bus.mem_side_ports

    def connectMemSideBus(self, bus):
        self.mem_side = bus.cpu_side_ports

class L3Cache(PrefetchCache):
    """L3 Cache with default values"""

    size = '40960KB'
    assoc = 12
    tag_latency = 67
    response_latency = 67
    response_latency = 1
    mshrs = 192
    # tgts_per_mshr = 16
    # write_buffers = 256

    clusivity = 'mostly_excl'

    def __init__(self):
        super(L3Cache, self).__init__()

    def connectCPUSideBus(self, bus):
        self.cpu_side = bus.mem_side_ports

    def connectMemSideBus(self, bus):
        self.mem_side = bus.cpu_side_ports

