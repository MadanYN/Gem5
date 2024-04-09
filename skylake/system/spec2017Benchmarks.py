import m5
from m5.objects import *

gem5_dir = '/cdt/gem5/'
spec_dir = '/cdt/cpu2017-1.1.9/benchspec/CPU'
out_dir = '/cdt/gem5/m5out/skylake-spec2017'

x86_suffix = '_base.mytest-m64'

# 600.perlbench_s
perlbench = Process()
perlbench.executable = '600.perlbench_s/exe/perlbench_s' + x86_suffix
perlbench.cmd = [perlbench.executable] + ['-I./lib', 'checkspam.pl', '2500', '5', '25', '11', '150', '1', '1', '1', '1']

# 602.gcc_s
gcc = Process()
gcc.executable = '602.gcc_s/exe/sgcc' + x86_suffix
gcc.cmd = [gcc.executable] + ['gcc-pp.c', '-03', '-finline-limit=0', '-fif-conversion', '-fif-conversion2', '-o gcc-pp.opts-O3_-finline-limit_0_-fif-conversion_-fif-conversion2.s']
