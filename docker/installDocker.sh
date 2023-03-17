#! /bin/bash
sudo apt update -y
sudo apt install python3-pip -y
sudo -H pip install --upgrade pip
sudo apt install git -y
apt-get update -y
apt-get install apt-transport-https -y ca-certificates -y curl -y gnupg -y lsb-release -y
mkdir -m 0755 -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/lin>
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

apt-get update -y
chmod a+r /etc/apt/keyrings/docker.gpg
apt-get update -y
apt-get install docker-ce -y docker-ce-cli -y containerd.io -y docker-buildx-plugin -y docker-compose-plugin -y