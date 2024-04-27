import m5
from m5.objects import *

gem5_dir = '/cdt/gem5/'
spec_dir = '/cdt/cpu2017-1.1.9/benchspec/CPU/'
out_dir = '/cdt/gem5/m5out/skylake-spec2017'

x86_suffix = '_base.mytest-m64'

'''intspeed benchmarks'''

# 600.perlbench_s
perlbench = Process()
perlbench.executable = spec_dir + '600.perlbench_s/exe/perlbench_s' + x86_suffix
perlbench.cmd = [perlbench.executable] + ['-I./lib', spec_dir + '500.perlbench_r/data/refrate/input/' + 'checkspam.pl', '2500', '5', '25', '11', '150', '1', '1', '1', '1']

# 602.gcc_s
gcc = Process()
gcc.executable = spec_dir + '602.gcc_s/exe/sgcc' + x86_suffix
gcc.cmd = [gcc.executable] + ['-I/usr/include/linux', spec_dir + '502.gcc_r/data/refspeed/input/' + 'gcc-pp.c', '-O3', '-finline-limit=0', '-fif-conversion', '-fif-conversion2', '-o gcc-pp.opts-O3_-finline-limit_0_-fif-conversion_-fif-conversion2.s']
# gcc.cmd = [gcc.executable] + [spec_dir + '502.gcc_r/data/test/input/' + 't1.c', '-O3', '-finline-limit=50000', '-o', 't1.opts-O3_-finline-limit_50000.s'] 

# 605.mcf_s
mcf = Process()
mcf.executable = spec_dir + '605.mcf_s/exe/mcf_s' + x86_suffix
mcf.cmd = [mcf.executable] + [spec_dir + '505.mcf_r/data/test/input/' + 'inp.in']

# 620.omnetpp_s
omnetpp = Process()
omnetpp.executable = spec_dir + '620.omnetpp_s/exe/omnetpp_s' + x86_suffix
omnetpp.cmd = [omnetpp.executable] + ['-c', 'General', '-r', '0']

# 623.xalancbmk_s
xalancbmk = Process()
xalancbmk.executable = spec_dir + '623.xalancbmk_s/exe/xalancbmk_s' + x86_suffix
xalancbmk.cmd = [xalancbmk.executable] + ['-v', '523.xalancbmk_r/data/test/input/' + 'test.xml', '523.xalancbmk_r/data/test/input/' + 'xalanc.xsl']


# 625.x256_s
x264 = Process()
x264.executable = spec_dir + '625.x264_s/exe/x264_s' + x86_suffix
x264.cmd = [x264.executable] + ['--dumpyuv', '50', '--frames', '156', '-o', spec_dir + '525.x264_r/data/test/input/' + 'BuckBunny.264', 'BuckBunny.yuv', '1280x720']

# 631.deepsjeng_s
deepsjeng = Process()
deepsjeng.executable = spec_dir + '631.deepsjeng_s/exe/deepsjeng_s' + x86_suffix
deepsjeng.cmd = [deepsjeng.executable] + [spec_dir + '631.deepsjeng_s/data/test/input/' + 'test.txt']

# 641.leela_s
leela = Process()
leela.executable = spec_dir + '641.leela_s/exe/leela_s' + x86_suffix
leela.cmd = [leela.executable] + [spec_dir + '541.leela_r/data/test/input/' + 'test.sgf']

# 648.exchange2_s
exchange2 = Process()
exchange2.executable = spec_dir + '648.exchange2_s/exe/exchange2_s' + x86_suffix
exchange2.cmd = [exchange2.executable] + ['0']

# 657.xz_s
xz = Process()
xz.executable = spec_dir + '657.xz_s/exe/xz_s' + x86_suffix
xz.cmd = [xz.executable] + [spec_dir + '557.xz_r/data/all/input/' + 'cpu2006docs.tar.xz', '4', '055ce243071129412e9dd0b3b69a21654033a9b723d874b2015c774fac1553d9713be561ca86f74e4f16f22e664fc17a79f30caa5ad2c04fbc447549c2810fae', ' 1548636', '1555348', '0' ]


'''fprate benchmarks'''

# 603.bwaves_s
bwaves = Process()
bwaves.executable = spec_dir + '603.bwaves_s/exe/speed_bwaves' + x86_suffix
bwaves.cmd = [bwaves.executable] + ['bwaves_1', '<', spec_dir + '503.bwaves_r/data/test/input' + 'bwaves_1.in'] 

# 607.cactuBSSN_s
cactuBSSN = Process()
cactuBSSN.executable = spec_dir + '607.cactuBSSN_s/exe/cactuBSSN_s' + x86_suffix
cactuBSSN.cmd = [cactuBSSN.executable] + [spec_dir + '507.cactuBSSN_r/data/test/input/' + 'spec_test.par']


# 619.lbm_s
lbm = Process()
lbm.executable = spec_dir + '619.lbm_s/exe/lbm_s' + x86_suffix
lbm.cmd = [lbm.executable] + ['20', 'reference.dat', '0', '1', spec_dir + '619.lbm_s/data/test/input/' + '200_200_260_ldc.of']

# 621.wrf_s
wrf = Process()
wrf.executable = spec_dir + '621.wrf_s/exe/wrf_s' + x86_suffix
wrf.cmd = [wrf.executable]


# 627.cam4_s
cam4 = Process()
cam4.executable = spec_dir + '627.cam4_s/exe/cam_s' + x86_suffix
cam4.cmd = [cam4.executable]

# 628.pop2_s
pop2 = Process()
pop2.executable = spec_dir + '628.pop2_s/exe/speed_pop2' + x86_suffix
pop2.cmd = [pop2.executable]

# 638.imagick_s
imagick = Process()
imagick.executable = spec_dir + '638.imagick_s/exe/imagick_s' + x86_suffix
imagick.cmd = [imagick.executable] + ['-limit', 'disk', '0', spec_dir + '538.imagick_r/data/test/input/' 'test_input.tga', '-shear', '25', '-resize', '640x480', '-negate', '-alpha', 'Off', 'test_output.tga']

# 644.nab_s
nab = Process()
nab.executable = spec_dir + '644.nab_s/exe/nab_s' + x86_suffix
nab.cmd = [nab.executable] + [spec_dir + '544.nab_r/data/test/input/hkrdenq/hkrdenq' '1930344093', '1000']

# 649.fotonik3d_s
fotonik3d = Process()
fotonik3d.executable = spec_dir + '649.fotonik3d_s/exe/fotonik3d_s' + x86_suffix
fotonik3d.cmd = [fotonik3d.executable]

# 654.roms_s
roms = Process()
roms.executable = spec_dir + '654.roms_s/exe/sroms' + x86_suffix
roms.cmd = [roms.executable] + [ '<', spec_dir + '554.roms_r/data/test/input/ocean_benchmark0.in.x']
