import sys
sys.path.append('/cdt/gem5/configs/')
import m5
from m5.objects import *
import common
from common import Options

import argparse
import optparse
from se  import MySystem
from core import *

import spec2017Benchmarks

#valid_configs = [VerbatimCPU, TunedCPU, UnConstrainedCPU]
#valid_configs = {cls.__name__[:-3]:cls for cls in valid_configs}

#parser = argparse.ArgumentParser()
#parser.add_argument('config', choices = valid_configs.keys())
#parser.add_argument('binary', type = str, help = "Path to binary to run")
#args = parser.parse_args()

parser = argparse.ArgumentParser()
Options.addCommonOptions(parser)
Options.addSEOptions(parser)

parser.add_argument("-b", "--benchmark", type=str, default="", help="The SPEC benchmark to be loaded.")
parser.add_argument("--isa", type=str, default="", help="ISA of the target machine")
parser.add_argument("--benchmark_stdout", type=str, default="", help="Absolute path for stdout redirection for the benchmark.")
parser.add_argument("--benchmark_stderr", type=str, default="", help="Absolute path for stderr redirection for the benchmark.")

options = parser.parse_args()

if options.benchmark:
    print('Selected SPEC CPU2017 benchmark', end='')

    # Integer benchmarks
    if options.benchmark == 'perlbench':
        print('--> perlbench')
        process = spec2017Benchmarks.perlbench
    elif options.benchmark == 'gcc':
        print('--> gcc')
        process = spec2017Benchmarks.gcc
    elif options.benchmark == 'mcf':
        print('--> mcf')
        process = spec2017Benchmarks.mcf
    elif options.benchmark == 'omnetpp':
        print('--> omnetpp')
        process = spec2017Benchmarks.omnetpp
    elif options.benchmark == 'xalancbmk':
        print('--> xalancbmk')
        process = spec2017Benchmarks.xalancbmk
    elif options.benchmark == 'x264':
        print('--> x264')
        process = spec2017Benchmarks.x264
    elif options.benchmark == 'deepsjeng':
        print('--> deepsjeng')
        process = spec2017Benchmarks.deepsjeng
    elif options.benchmark == 'leela':
        print('--> leela')
        process = spec2017Benchmarks.leela
    elif options.benchmark == 'exchange2':
        print('--> exchange2')
        process = spec2017Benchmarks.exchange2
    elif options.benchmark == 'xz':
        print('--> xz')
        process = spec2017Benchmarks.xz
    
    # Floating-Point benchmarks
    elif options.benchmark == 'bwaves':
        print('--> bwaves')
        process = spec2017Benchmarks.bwaves
    elif options.benchmark == 'cactuBSSN':
        print('--> cactuBSSN')
        process = spec2017Benchmarks.cactuBSSN
    elif options.benchmark == 'lbm':
        print('--> lbm')
        process = spec2017Benchmarks.lbm
    elif options.benchmark == 'wrf':
        print('--> wrf')
        process = spec2017Benchmarks.wrf
    elif options.benchmark == 'cam4':
        print('--> cam4')
        process = spec2017Benchmarks.cam4
    elif options.benchmark == 'pop2':
        print('--> pop2')
        process = spec2017Benchmarks.pop2
    elif options.benchmark == 'imagick':
        print('--> imagick')
        process = spec2017Benchmarks.imagick
    elif options.benchmark == 'nab':
        print('--> nab')
        process = spec2017Benchmarks.nab
    elif options.benchmark == 'fotonik3d':
        print('--> fotonik3d')
        process = spec2017Benchmarks.fotonik3d
    elif options.benchmark == 'roms':
        print('--> roms')
        process = spec2017Benchmarks.roms
    else:
        print('No recognized SPEC2017 benchmark selected! Exiting.')
        sys.exit(1)
else:
    print(sys.stderr, "Need --benchmark switch to specify SPEC CPU2017 workload. Exiting!\n")
    sys.exit(1)



class TestSystem(MySystem):
    _CPUModel = TunedCPU()
    def __init__(self, isa):
        if isa == 'ARM':
            self._CPUModel.isa = ArmISA()
        elif isa == 'RISCV':
            self._CPUModel.isa = RiscvISA()
        else:
            self._CPUModel.isa = X86ISA()

# #binary = 'tests/my_tests/primes_arm'
# binary = 'tests/test-progs/hello/bin/x86/linux/hello'
system = TestSystem(options.isa)
print(f"ISA --> {options.isa}")
system.workload = SEWorkload.init_compatible(process.executable)

# process = Process() 
system.cpu.workload = process 
#    print(process.cmd)
# process.cmd = [binary]
# system.cpu.workload = process
system.cpu.createThreads()

root = Root(full_system = False, system = system)
m5.instantiate()
exit_event = m5.simulate()

print('Exiting @ tick {} because {}'
      .format(m5.curTick(), exit_event.getCause()))
