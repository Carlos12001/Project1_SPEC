#!/bin/bash

# Parámetros
OUTPUT_DIR=$1
ARCH=$2
CPU_TYPE=$3
L1D_SIZE=$4
L1I_SIZE=$5
L2_SIZE=$6
L1D_ASSOC=$7
L1I_ASSOC=$8
L2_ASSOC=$9
CACHELINE_SIZE=${10}
BP_TYPE=${11}
REPLACEMENT_POLICY=${12}

# Rutas base y de gem5
GEM5_DIR="/home/carlos/Documents/gem5/gem5"
GEM5_BINARY="$GEM5_DIR/build/$ARCH/gem5.opt"

# Comando de ejecución
time $GEM5_BINARY -d $OUTPUT_DIR $GEM5_DIR/configs/deprecated/example/se.py \
-c ./src/benchmark -o ./data/test.txt -I 100000000 \
--cpu-type=$CPU_TYPE --caches --l2cache \
--l1d_size=$L1D_SIZE --l1i_size=$L1I_SIZE --l2_size=$L2_SIZE \
--l1d_assoc=$L1D_ASSOC --l1i_assoc=$L1I_ASSOC --l2_assoc=$L2_ASSOC \
--cacheline_size=$CACHELINE_SIZE \
--bp-type=$BP_TYPE \
--replacement-policy=$REPLACEMENT_POLICY
