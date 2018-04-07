#!/usr/bin/env bash

combustion_lib_path="$(pwd)/dependencies/combustion/target/release/libcombustion_r.so"

function installSystemDependencies () {
  # Get the sytem dependencies
  sudo apt-get install -y \
    git \
    python3 \
    python3-pip

  if [ $? -ne 0 ]; then
    echo "Failed to install system dependencies!!"
    exit 1
  fi

  mkdir -p "dependencies"

  wget -O "dependencies/rust_installer.sh" "https://sh.rustup.rs"

  if [ $? -ne 0 ]; then
    echo "Failed to download Rust!!"
    exit 1
  fi

  chmod +x "dependencies/rust_installer.sh"
  "./dependencies/rust_installer.sh" -y

  if [ $? -ne 0 ]; then
    echo "Failed to download Rust!!"
    exit 1
  fi

  pip3 install cffi

  if [ $? -ne 0 ]; then
    echo "Failed to install Python CFFI via pip!!"
    exit 1
  fi
}

function installCombustion () {
  mkdir -p "dependencies"
  cd "dependencies"

  git clone -b "feature/compileOnLinux" "https://github.com/brainthinks/combustion.git"

  if [ $? -ne 0 ]; then
    echo "Failed to download combustion!!"
    exit 1
  fi

  cd "combustion"
  cargo build --release

  if [ $? -ne 0 ]; then
    echo "Failed to build combustion!!"
    exit 1
  fi

  cd "../.."
}
