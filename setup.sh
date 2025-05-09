#!/bin/bash

# Check if running sudo
if [ "$EUID" -ne 0 ]; then
  echo "Please run as root"
  exit
fi

# Check distro
DISTRO=$(cat </etc/os-release | grep -oP 'ID=\K\w+' | head -1)

if [ "$DISTRO" != "fedora" ]; then
  echo "This script is for Fedora only"
  exit 1
fi

# Setup confirmation message
read -r -p "This will add a repo file. Continue? [y/N] " choice

case "$choice" in
y | Y)
  echo "Starting script..."
  ;;
n | N)
  echo "Stopping script..."
  exit 1
  ;;
*)
  echo "Invalid option. Stopping script..."
  exit 1
  ;;
esac

# Add repository file
cat > /etc/yum.repos.d/_copr:copr.fedorainfracloud.org:relativesure:all-packages.repo << 'EOF'
[copr:copr.fedorainfracloud.org:relativesure:all-packages]
EOF
name=Copr repo for all-packages owned by relativesure
baseurl=https://download.copr.fedorainfracloud.org/results/relativesure/all-packages/fedora-$releasever-$basearch/
type=rpm-md
skip_if_unavailable=True
gpgcheck=1
gpgkey=https://download.copr.fedorainfracloud.org/results/relativesure/all-packages/pubkey.gpg
repo_gpgcheck=0
enabled=1
enabled_metadata=1
EOF
