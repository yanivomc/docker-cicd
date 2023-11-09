#!/bin/bash
git config --global --add safe.directory /src/linux/kernel/linux
cd  /src/linux/kernel/linux
./build_sx_kernel.sh -c sx4000
# Check if the last command was successful (exit code 0)
if [ $? -eq 0 ]; then
    ./build_sx_kernel.sh -c sx4000 mod_prep
else
    echo "Kernel build failed, not proceeding with mod_prep"
    exit 1
fi
cd  /src/linux/kernel/bin/sx4000/arch/arm64/boot
gzip -c Image.015 > ./kernel.Image.gz && rm -rf Image.015
#Creating an output folder at the local workrepo for u-boot.artifactor image to copy the bin file
mkdir -p /src/linux/kernel/linux/output/
yes | cp -rf  kernel.Image.gz /src/linux/kernel/linux/output/
yes | cp -rf /src/linux/kernel/bin /src/linux/kernel/linux/output/bin
mkdir -p /src/linux/kernel/linux/output/arch/
yes | cp -rf /src/linux/kernel/linux/arch/arm64 /src/linux/kernel/linux/output/arch/
yes | cp -rf /src/linux/kernel/linux/include /src/linux/kernel/linux/output/include
yes | cp -rf /src/linux/kernel/linux/scripts /src/linux/kernel/linux/output/scripts
yes | cp -rf /src/linux/kernel/linux/Makefile /src/linux/kernel/linux/output/Makefile

exec $@
