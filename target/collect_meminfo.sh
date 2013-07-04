DIRNAME=`date +%F_%H-%M`
TIME=$1
DIR=/data/debug/meminfo/"$DIRNAME"
mkdir -p "$DIR";
cd "$DIR";
I=0
echo "Recording memory usage in \""$DIRNAME"\""
while [ $I -lt $TIME ]
do
  FNAME=`date +%F_%H-%M-%S`
  touch "$FNAME".log
  procrank > "$FNAME".log;
  #dumpsys meminfo > "$FNAME".log;
  cat /proc/meminfo | grep MemFree >> "$FNAME".log;
  cat /proc/meminfo | grep Buffers >> "$FNAME".log;
  cat /proc/meminfo | grep Cached | grep -v Swap >> "$FNAME".log;
  cat /proc/meminfo | grep Slab >> "$FNAME".log;
  cat /proc/meminfo | grep Shmem >> "$FNAME".log;
  echo -n "Date: " >> "$FNAME".log;
  busybox date +"%d%m%y%H%M%S" >>"$FNAME".log;
  sleep 0.5
  I=$(expr $I + 1)
done

echo "Done!"

