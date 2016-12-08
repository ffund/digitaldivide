#!/bin/bash

mkdir -p tmp

IPERF_OK=$(dpkg-query -W --showformat='${Status}\n' iperf3 | grep "install ok installed")
if [ "" == "$IPERF_OK" ]; then
  # Install software prerequisites for validation
  sudo apt-get update
  sudo apt-get -y install iperf software-properties-common python-software-properties
  sudo add-apt-repository -y "ppa:patrickdk/general-lucid"
  sudo apt-get update 
  sudo apt-get -y install iperf3
fi

# Linux kernel tuning TODO
sudo sysctl -w net.core.rmem_max=134217728 
sudo sysctl -w net.core.wmem_max=134217728 
sudo sysctl -w net.ipv4.tcp_rmem="4096 87380 67108864"
sudo sysctl -w net.ipv4.tcp_wmem="4096 65536 67108864"


for trial in $(seq 0 10); do
  echo '[' `date` ']' " Ping test for trial $trial"
  # Test latency
  ping server -i 0.2 -c 100 > "tmp/ping-$trial.txt"

  # Test UL/DL speed
  # Server must be running 'iperf3 -s'
  echo '[' `date` ']' " UL/DL throughput test for trial $trial"
  iperf3 -c server -i 5 -t 60 -P 3 -w 50k --format k        > "tmp/ulrate-$trial.txt"
  iperf3 -c server -i 5 -t 60 -P 3 -w 50k -R --format k     > "tmp/dlrate-$trial.txt"

  # Test UL/DL jitter and packet loss
  # Server must be running 'iperf -s -u'
  echo '[' `date` ']' " Jitter/loss test for trial $trial"
  iperf -c server -u -b 100k -t 60 -l 180 -r  > "tmp/udp-$trial.txt"
done
#for trial in $(seq 0 1); do
#  iperf -c server -u -b 500k -t 90 -i 5 -l 90    > "/tmp/uljitter-$trial.txt"
#done

#sums = grep -n "[SUM]" dlrate-0.txt #all the lines with sum and the line num 
#csvthing = last "sum" * 12 - first and second sums divided by 10 #returns avg ignoring first 10 secs. make sure to only search under bandwidth


