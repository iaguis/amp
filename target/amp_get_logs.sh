#!/bin/sh
if [ "$#" -ne 2 ];
then
    echo "Usage: $(basename $0) measure_name output_dir"
    exit 1
fi

MEASUREMENT_NAME=$1
OUTPUT_DIR=$2

ADB=adb

$ADB pull /data/debug/meminfo/$MEASUREMENT_NAME $OUTPUT_DIR
