#Cache Architecture
from m5.objects import Cache
from Common import SimpleOpts

#Base class for creating L1 I & D caches
#Note : Read the Cache class to understand the member fields and methods
class L1Cache(Cache):
	def __init__(self, options=None):
		super(L1Cache, self).__init__()
		pass

	assoc = 2 #two-way set associvity
	tag_latency = 2 #cache hit latency
	data_latency = 2
	response_latency = 2
	mshrs = 4
	tgts_per_mshr = 20

	def connectCPU(self, cpu): #raises if connectCPU is not implemented in child classes
			raise NotImplementedError

	def connectBus(self, bus): #connects mem_size port of both i and d caches to membus
			self.mem_side = bus.cpu_side_ports


class L1ICache(L1Cache):
	SimpleOpts.add_option(
        "--l1i_size", help=f"L1 instruction cache size. Default: {size}"
    )
	def __init__(self, options=None):
		super(L1ICache, self).__init__(options)
		if not options or not options.l1i_size:
			return
		self.size = options.l1i_size

		size = '16kB'

	def connectCPU(self, cpu):
		self.cpu_side = cpu.icache_port

class L1DCache(L1Cache):
	SimpleOpts.add_option(
        "--l1d_size", help=f"L1 data cache size. Default: {size}"
    )

	def __init__(self, options=None):
		super(L1DCache, self).__init__(options)
		if not options or not options.l1d_size:
			return
		self.size = options.l1d_size

	size = '64kB'
	def connectCPU(self, cpu):
		self.cpu_side = cpu.dcache_port

class L2Cache(Cache):
	SimpleOpts.add_option("--l2_size", help=f"L2 cache size. Default: {size}")
	
	def __init__(self, options=None):
		super(L2Cache, self).__init__()
		if not options or not options.l2_size:
			return
		self.size = options.l2_size

	size = '256kB'
	assoc = 8
	tag_latency = 20
	data_latency = 20
	response_latency = 20
	mshrs = 20
	tgts_per_mshr = 12

	def connectCPUSideBus(self, bus):
		self.cpu_side = bus.mem_side_ports

	def connectMemSideBus(self, bus):
		self.mem_side = bus.cpu_side_ports
