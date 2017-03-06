

IPERF_OK=$(dpkg-query -W --showformat='${Status}\n' iperf3 | grep "install ok installed")
if [ "" == "$IPERF_OK" ]; then
  # Install software prerequisites for validation
  sudo apt-get update
  sudo apt-get -y install iperf software-properties-common python-software-properties screen vim
  sudo add-apt-repository -y "ppa:patrickdk/general-lucid"
  sudo apt-get update
  sudo apt-get -y install iperf3
fi

# Linux kernel tuning TODO
sudo sysctl -w net.core.rmem_max=134217728
sudo sysctl -w net.core.wmem_max=134217728
sudo sysctl -w net.ipv4.tcp_rmem="4096 87380 67108864"
sudo sysctl -w net.ipv4.tcp_wmem="4096 65536 67108864"

git clone https://github.com/csmithsalzberg/digitaldivide.git
cd digitaldivide/util
bash install.sh
