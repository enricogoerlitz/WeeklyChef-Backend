# Setup Linux

## Ubuntu-Desktop

sudo apt update && sudo apt upgrade
sudo apt install ubuntu-desktop

## Docker (<a>https://docs.docker.com/engine/install/ubuntu/</a>)

### 1. Setup

sudo apt-get update
sudo apt-get install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update

### 2. Install packages

sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

### 3. Test Hello-World

sudo docker run hello-world


## VS Code

Donwload (ARM64 - .deb)
https://code.visualstudio.com/download

cd Downloads/
sudo dpkg -i code_1.87.1-1709684532_arm64.deb 
