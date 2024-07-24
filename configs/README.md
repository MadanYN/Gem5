Directory: Gem5/configs
Author: Madan Y N
Year: 2024
email: madanyn3@gmail.com

* This directory contains simple_arm.py, simple_x86.py, o3_arm.py and o3_x86.py files that use the cache hierarchy described in caches.py
* These configs use the standard cpu models provided by gem5
* Sample command to launch simulation: *GEM5_DIR/build/ISA/gem5.{opt, fast, debug} simple_arm.py*
* To change any param you have to modify the .py file itself, command line options are not supported
* Output files are stored in *GEM5_DIR/m5out/* directory