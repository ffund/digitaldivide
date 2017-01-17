FOLDER="tmp"


for FOLDER in tmp-* ; do
  house=$(cut -f2 -d'-' <<< "$FOLDER")

  echo "Working on house $house"
  echo "type,trial,measure" > "$FOLDER"/"consolidate-$house".csv

  for tputtype in "dl"; do
    for file in "$FOLDER"/"$tputtype"rate-*; do
      lines=$(cat "$file" | grep "SUM" | head -12 | tail -10 )
      mBytes=$(echo -e "$lines" | grep "MBytes" |  awk '{sum+=$4} END {print sum}')
      kBytes=$(echo -e "$lines" | grep "KBytes" |  awk '{sum+=$4} END {print sum}')
      Bytes=$(echo $lines | grep " Bytes" |  awk '{sum+=$4} END {print sum}')
      [[  -z  $mBytes  ]] && mBytes=0
      [[  -z  $kBytes  ]] && kBytes=0
      [[  -z  $Bytes  ]] && Bytes=0
      begintime=$(cat "$file" | grep "SUM" | head -3 | tail -1 | awk '{print $2}' | cut -f1 -d'-')
      endtime=$(cat "$file" | grep "SUM" | head -12 | tail -1 | awk '{print $2}' | cut -f2 -d'-')
      throughput=$(bc <<< "scale=5; 8*($mBytes*1000 + $kBytes + $Bytes/1000)/($endtime - $begintime)" )
      mtype="$tputtype"rate
      trial=$(echo $file | awk -F'[-.]' '{print $3}')

      echo "$mtype,$trial,$throughput" >> "$FOLDER"/"consolidate-$house".csv
    done
  done

  for tputtype in "ul"; do
    for file in "$FOLDER"/"$tputtype"rate-*; do
      throughput=$(cat "$file" | grep "SUM" |  grep "receiver" | awk '{ print $6}')
      mtype="$tputtype"rate
      trial=$(echo $file | awk -F'[-.]' '{print $3}')
      echo "$mtype,$trial,$throughput" >> "$FOLDER"/"consolidate-$house".csv
    done
  done

  for file in "$FOLDER"/ping*; do

    mtype="latency"
    latency=$(cat $file | tail -1 | cut -d'/' -f5)
    trial=$(echo $file | awk -F'[-.]' '{print $3}')
    echo "$mtype,$trial,$latency" >> "$FOLDER"/"consolidate-$house".csv
  done

  for file in "$FOLDER"/udp*; do

    mtype="loss"
    loss=$(cat $file | grep '%' | tail -1 | cut -d'(' -f2 | cut -d'%' -f1 )
    trial=$(echo $file | awk -F'[-.]' '{print $3}')
    echo "$mtype,$trial,$loss" >> "$FOLDER"/"consolidate-$house".csv
  done

  for file in "$FOLDER"/udp*; do

    mtype="dljitter"
    dljitter=$(cat $file | grep '%' | tail -1 | awk '{print $9}')
    trial=$(echo $file | awk -F'[-.]' '{print $3}')
    echo "$mtype,$trial,$dljitter" >> "$FOLDER"/"consolidate-$house".csv

  done

  for file in "$FOLDER"/udp*; do

    mtype="uljitter"
    uljitter=$(cat $file | grep '%' | head -1 | awk '{print $9}')
    trial=$(echo $file | awk -F'[-.]' '{print $3}')
    echo "$mtype,$trial,$uljitter" >> "$FOLDER"/"consolidate-$house".csv
  done

done

