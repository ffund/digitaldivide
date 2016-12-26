# This script installs prerequisites on an Ubuntu 14.04 installation
# Run it as: bash install.sh

# Install geni-lib prerequisite: 
# From http://geni-lib.readthedocs.io/en/stable/intro/ubuntu.html
sudo apt-get update
sudo apt-get -y install mercurial python-pip python-m2crypto python-dateutil python-lxml \
  python-dev libxmlsec1 xmlsec1 libxmlsec1-openssl python-setuptools python-openssl libffi-dev 

cd ~  
hg clone http://bitbucket.org/barnstorm/geni-lib
cd geni-lib
hg update -C 0.9-DEV
sudo python setup.py install
cd ~

# We need pandas version >= 0.16.1. 
# The version in Ubuntu 14.04 repository is too old. So we get it from PyPI
sudo pip install pandas
