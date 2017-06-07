#!/bin/sh

# Install packages
sudo apt-get -y update
sudo apt-get install -y python-dev
sudo apt-get install -y python-pip

# Clone repo
git clone https://github.com/BertilGrelsson/MyCloud.git

# Setup environment
cd MyCloud
./setup.sh

# Run monitor instrument
python monitor/instrument.py

# Run worker
python worker/worker.py
