#!/bin/bash

# Install software prerequisites for validation
sudo apt-get update
sudo apt-get -y install iperf software-properties-common python-software-properties
sudo add-apt-repository -y "ppa:patrickdk/general-lucid"
sudo apt-get update 
sudo apt-get -y install iperf3

# Linux kernel tuning TODO

for trial in $(seq 0 9); do
  # Test latency
  ping server -i 0.2 -c 100 > "/tmp/ping-$trial.txt"

  # Test UL/DL speed
  # Server must be running 'iperf3 -s'
  iperf3 -c server -i 5 -t 60 -P 3 -w 50k        > "/tmp/ulrate-$trial.txt"
  iperf3 -c server -i 5 -t 60 -P 3 -w 50k -R     > "/tmp/dlrate-$trial.txt"

  # Test UL/DL jitter and packet loss
  # Server must be running 'iperf -s -u'
  iperf -c server -u -b 500k -t 90 -i 5 -l 90    > "/tmp/uljitter-$trial.txt"
done
