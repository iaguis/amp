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
  dumpsys meminfo > "$FNAME".log;
  cat /proc/meminfo | grep MemFree >> "$FNAME".log;
  sleep 1
  I=$(expr $I + 1)
done

echo "Done!"

