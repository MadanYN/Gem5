Directory: Gem5/skylake/system
Author: Madan Y N
Year: 2014
email: madanyn3@gmail.com

* This directory contains skykake.py, se.py, core.py and caches.py that describe the Intel Skylake architecture to run simulations in Gem5 SE(System-call Emulation) mode.
* launch-spec2017.sh file automates launching simulation on one or more of the spec2017 benchmarks and skylake-spec2017.py and spec2017Benchmarks are helper files
* Refer to the bash file or run *./launch-spec2017.sh* to know how to run simulations
* The commands to launch correct spec2017 benchmark can be refferd here *https://tosiron.com/papers/2018/SPEC2017_commands.pdf*
* The simulation results can be found in *GEM5_DIR/m5out/spec2017/BENCHMARK_NAME/*
* The files fs_tools.py, fs.py, MESI_Two_Level.py, MI_example_caches.py and ruby_system.py are part of the clones repository from *https://github.com/darchr/gem5-skylake-config*. You can safely ignore them and refer to the repository for more details