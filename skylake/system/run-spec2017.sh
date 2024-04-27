#!/bin/bash
#
# run-spec2017.sh
# Author: Madan Y N Email: madanyn3@gmail.com
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
 
 
############ DIRECTORY VARIABLES: MODIFY ACCORDINGLY #############
GEM5_DIR=/cdt/gem5/                          # Install location of gem5
SPEC_DIR=/cdt/cpu2017-1.1.9/                  # Install location of your SPEC2006 benchmarks
##################################################################
 
ARGC=$# # Get number of arguments excluding arg0 (the script itself). Check for help message condition.
if [[ "$ARGC" < 1 || "$ARGC" > 2 ]]; then # Bad number of arguments.
   # echo "This program comes with ABSOLUTELY NO WARRANTY; for details see <http://www.gnu.org/licenses/>."
   echo "This is free software, and you are welcome to redistribute it under certain conditions; see <http://www.gnu.org/licenses/> for details."
   echo ""
    echo "Author: Madan Y N"
    echo "madanyn3@gmail.com"
    echo ""
    echo "This script runs a single gem5 simulation of one or more SPEC CPU2017 benchmarks"
    echo ""
    echo "USAGE: run-spec2017 <BENCHMARK> <OUTPUT_DIR>"
    echo "EXAMPLE: ./run-spec2017.sh gcc /FULL/PATH/TO/output_dir"
    echo ""
    echo "A single --help help or -h argument will bring this message back."
    exit
fi
 
# Get command line input. We will need to check these.
BENCHMARK=$1                    # Benchmark name, e.g. bzip2
OUTPUT_DIR=/cdt/gem5/m5out/spec2017/$BENCHMARK

if [[ "$ARGC" == 2 ]]; then # Additional flag for debug and other functionalities
    FLAG=$2
fi
 
######################### BENCHMARK CODENAMES ####################

# intspeed
PERLBENCH_CODE=600.perlbench_s
GCC_CODE=602.gcc_s
MCF_CODE=605.mcf_s
OMNETPP_CODE=620.omnetpp_s
XALANCBMK_CODE=623.xalancbmk_s
X264_CODE=625.x264_s
DEEPSJENG_CODE=631.deepsjeng_s
LEELA_CODE=641.leela_s
EXCHANGE2_CODE=648.exchange2_s
XZ_CODE=657.xz_s

# fpspeed
BWAVES_CODE=bwaves_s
CACTUBSSN_CODE=607.cactuBSSN_S
LBM_CODE=619.lbm_s
WRF_CODE=621.wrf_s
CAM4_CODE=627.cam4_s
IMAGICK_CODE=638.imagick_s
NAB_CODE=644.nab_s
FOTONIK3D_CODE=649.fotonik3d_s
ROMS_CODE=654.roms_s

##################################################################
 
# Check BENCHMARK input
#################### BENCHMARK CODE MAPPING ######################
BENCHMARK_CODE="none"
 
if [[ "$BENCHMARK" == "perlbench" ]]; then
    BENCHMARK_CODE=$PERLBENCH_CODE
fi
if [[ "$BENCHMARK" == "gcc" ]]; then
    BENCHMARK_CODE=$GCC_CODE
fi
if [[ "$BENCHMARK" == "mcf" ]]; then
    BENCHMARK_CODE=$MCF_CODE
fi
if [[ "$BENCHMARK" == "omnetpp" ]]; then
    BENCHMARK_CODE=$OMNETPP_CODE
fi
if [[ "$BENCHMARK" == "xalancbmk" ]]; then
    BENCHMARK_CODE=$XALANCBMK_CODE
fi
if [[ "$BENCHMARK" == "x264" ]]; then
    BENCHMARK_CODE=$X264_CODE
fi
if [[ "$BENCHMARK" == "deepsjeng" ]]; then
    BENCHMARK_CODE=$DEEPSJENG_CODE
fi
if [[ "$BENCHMARK" == "leela" ]]; then
    BENCHMARK_CODE=$LEELA_CODE
fi
if [[ "$BENCHMARK" == "exchange2" ]]; then
    BENCHMARK_CODE=$EXCHANGE2_CODE
fi
if [[ "$BENCHMARK" == "xz" ]]; then
    BENCHMARK_CODE=$XZ_CODE
fi

# fpspeed
if [[ "$BENCHMARK" == "bwaves" ]]; then
    BENCHMARK_CODE=$BWAVES_CODE
fi
if [[ "$BENCHMARK" == "cactuBSSN" ]]; then
    BENCHMARK_CODE=$CACTUBSSN_CODE
fi
if [[ "$BENCHMARK" == "lbm" ]]; then
    BENCHMARK_CODE=$LBM_CODE
fi
if [[ "$BENCHMARK" == "wrf" ]]; then
    BENCHMARK_CODE=$WRF_CODE
fi
if [[ "$BENCHMARK" == "cam4" ]]; then
    BENCHMARK_CODE=$CAM4_CODE
fi
if [[ "$BENCHMARK" == "pop2" ]]; then
    BENCHMARK_CODE=$POP2_CODE
fi
if [[ "$BENCHMARK" == "imagick" ]]; then
    BENCHMARK_CODE=$IMAGICK_CODE
fi
if [[ "$BENCHMARK" == "nab" ]]; then
    BENCHMARK_CODE=$NAB_CODE
fi
if [[ "$BENCHMARK" == "fotonik3d" ]]; then
    BENCHMARK_CODE=$FOTONIK3D_CODE
fi
if [[ "$BENCHMARK" == "roms" ]]; then
    BENCHMARK_CODE=$ROMS_CODE
fi

# Sanity check
if [[ "$BENCHMARK_CODE" == "none" ]]; then
    echo "Input benchmark selection $BENCHMARK did not match any known SPEC CPU2017 benchmarks! Exiting."
    exit 1
fi
##################################################################
 
# Check OUTPUT_DIR existence
if [[ !(-d "$OUTPUT_DIR") ]]; then
    echo "Output directory $OUTPUT_DIR does not exist! Exiting."
    exit 1
fi
 
RUN_DIR=$SPEC_DIR/benchspec/CPU/$BENCHMARK_CODE/run/run_base_test_mytest-m64.0001     # Run directory for the selected SPEC benchmark
SCRIPT_OUT=$OUTPUT_DIR/runscript.log                                                                    # File log for this script's stdout henceforth
 
################## REPORT SCRIPT CONFIGURATION ###################
 
echo "Command line:"                                | tee $SCRIPT_OUT
echo "$0 $*"                                        | tee -a $SCRIPT_OUT
echo "================= Hardcoded directories ==================" | tee -a $SCRIPT_OUT
echo "GEM5_DIR:                                     $GEM5_DIR" | tee -a $SCRIPT_OUT
echo "SPEC_DIR:                                     $SPEC_DIR" | tee -a $SCRIPT_OUT
echo "==================== Script inputs =======================" | tee -a $SCRIPT_OUT
echo "BENCHMARK:                                    $BENCHMARK" | tee -a $SCRIPT_OUT
echo "OUTPUT_DIR:                                   $OUTPUT_DIR" | tee -a $SCRIPT_OUT
echo "==========================================================" | tee -a $SCRIPT_OUT
##################################################################
 
 
#################### LAUNCH GEM5 SIMULATION ######################
echo ""
echo "Changing to SPEC benchmark runtime directory: $RUN_DIR" | tee -a $SCRIPT_OUT
cd $RUN_DIR
 
echo "" | tee -a $SCRIPT_OUT
echo "" | tee -a $SCRIPT_OUT
echo "--------- Here goes nothing! Starting gem5! ------------" | tee -a $SCRIPT_OUT
echo "" | tee -a $SCRIPT_OUT
echo "" | tee -a $SCRIPT_OUT
 
# Actually launch gem5!

if [[ $FLAG == "--debug" ]]; then # gem5 in debug mode
    echo "Initiating gem5 debug mode"
    OUTPUT_DIR=/cdt/gem5/m5out/spec2017/$BENCHMARK/debug
    $GEM5_DIR/build/X86/gem5.debug --outdir=$OUTPUT_DIR $GEM5_DIR/configs/my_projects/Gem5/skylake/system/skylake-spec2017.py --benchmark=$BENCHMARK --benchmark_stderr=$OUTPUT_DIR/$BENCHMARK.err | tee -a $SCRIPT_OUT
elif [[ $FLAG == "--fast" ]]; then # gem5 fast
    echo "Running gem5 fast"
    OUTPUT_DIR=/cdt/gem5/m5out/spec2017/$BENCHMARK/debug
    $GEM5_DIR/build/X86/gem5.fast --outdir=$OUTPUT_DIR $GEM5_DIR/configs/my_projects/Gem5/skylake/system/skylake-spec2017.py --benchmark=$BENCHMARK --benchmark_stderr=$OUTPUT_DIR/$BENCHMARK.err | tee -a $SCRIPT_OUT
else
    echo "Running gem5 opt"
    $GEM5_DIR/build/X86/gem5.opt --outdir=$OUTPUT_DIR $GEM5_DIR/configs/my_projects/Gem5/skylake/system/skylake-spec2017.py --benchmark=$BENCHMARK --benchmark_stderr=$OUTPUT_DIR/$BENCHMARK.err | tee -a $SCRIPT_OUT
fi
