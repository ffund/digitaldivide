#!/bin/bash

mkdir -p tmp

for trial in $(seq 0 10); do
  echo '[' `date` ']' " Ping test for trial $trial"
  # Test latency
  ping server -i 0.2 -c 100 > "tmp/ping-$trial.txt"

  # Test UL/DL speed
  # Server must be running 'iperf3 -s'
  echo '[' `date` ']' " UL/DL throughput test for trial $trial"
  iperf3 -c server -i 5 -t 60 -P 3 --format k        > "tmp/ulrate-$trial.txt"
  iperf3 -c server -i 5 -t 60 -P 3 -R --format k     > "tmp/dlrate-$trial.txt"

  # Test UL/DL jitter and packet loss
  # Server must be running 'iperf -s -u'
  echo '[' `date` ']' " Jitter/loss test for trial $trial"
  iperf -c server -u -b 100k -t 60 -l 180 -r  > "tmp/udp-$trial.txt"
done


