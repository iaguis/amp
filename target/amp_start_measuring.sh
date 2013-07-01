#!/bin/sh

if [ "$#" -ne 1 ] || [ -z "`echo $1 | egrep '^[0-9]+$'`" ];
then
    echo "Usage: $(basename $0) measure_time"
    exit 1
fi

TIME=$1

ADB=adb

# wait until device ready
sleep 1

$ADB push $(dirname $0)/collect_meminfo.sh /data/collect_meminfo.sh

$ADB shell sh /data/collect_meminfo.sh $TIME

